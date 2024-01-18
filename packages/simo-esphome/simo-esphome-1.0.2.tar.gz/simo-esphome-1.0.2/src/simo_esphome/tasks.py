import os
import json
import sys
import shutil
import logging
import subprocess
from celeryc import celery_app
from logging.handlers import RotatingFileHandler
from django.conf import settings
from django.utils import timezone
from simo.core.utils.model_helpers import get_log_file_path
from .models import ESPDevice




@celery_app.task
def rebuild_firmware(esp_device_id):
    esp_device = ESPDevice.objects.get(id=esp_device_id)
    esp_device.firmware_status = 'compiling'
    esp_device.save()


    old_version = esp_device.compiled_version
    esp_device.compiled_version = str(timezone.now().timestamp())

    esphome_dir = os.path.join(settings.MEDIA_ROOT, 'esphome')
    yaml_config_path = os.path.join(esphome_dir, '%s.yaml' % esp_device.name)
    if not os.path.exists(esphome_dir):
        os.makedirs(esphome_dir)

    config_yaml = esp_device.get_current_config()
    with open(yaml_config_path, 'w') as yaml_config_f:
        yaml_config_f.write(config_yaml)

    logger = logging.getLogger(
        "ESP Device Logger [%d]" % esp_device.id
    )
    logger.propagate = False
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(message)s',
            "%m-%d %H:%M:%S"
        )
        formatter.converter = \
            lambda *args, **kwargs: timezone.localtime().timetuple()
        file_handler = RotatingFileHandler(
            get_log_file_path(esp_device), maxBytes=102400,  # 100KB
            backupCount=3, encoding='utf-8',
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    proc = subprocess.Popen(
        ['esphome', 'compile', '%s.yaml' % esp_device.name],
        cwd=esphome_dir, env=os.environ.copy(),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    with proc.stdout as stdout:
        for line in iter(stdout.readline, b''):
            logger.log(logging.INFO, line.decode().rstrip('\n'))

    status = proc.wait()
    if status:
        esp_device.firmware_status = 'out_of_date'
        esp_device.save(update_fields=['firmware_status'])
        return

    with open(
        os.path.join(
            esphome_dir, '.esphome', 'idedata', '%s.json' % esp_device.name
        )
    ) as f:
        idedata = json.loads(f.read())

    firmware_offset = "0x10000" if esp_device.platform == 'esp32' else "0x0"
    parts = [
        {'path': idedata['prog_path'][:-4] + '.bin', 'offset': firmware_offset},
    ]
    parts.extend(idedata['extra']['flash_images'])

    for part in parts:
        filename = part['path'][part['path'].rfind('/') + 1:]
        if part['path'].startswith(settings.MEDIA_ROOT):
            build_folder = os.path.join(
                esphome_dir, '%s_build_%s' % (
                    esp_device.name, esp_device.compiled_version
                )
            )
            if not os.path.exists(build_folder):
                os.makedirs(build_folder)
            shutil.copy(
                part['path'],
                os.path.join(build_folder, filename)
            )
            try:
                # remove old build
                shutil.rmtree(os.path.join(
                    esphome_dir, '%s_build_%s' % (
                        esp_device.name, old_version
                    )
                ))
            except:
                pass
            part['path'] = '%sesphome/%s_build_%s/%s' % (
                settings.MEDIA_URL, esp_device.name,
                esp_device.compiled_version, filename
            )
        else:
            if not os.path.exists(os.path.join(esphome_dir, filename)):
                shutil.copy(part['path'], os.path.join(esphome_dir, filename))
            part['path'] = settings.MEDIA_URL + 'esphome/' + filename

    manifest_data = {
        'name': esp_device.name,
        'version': esp_device.compiled_version,
        'new_install_prompt_erase': False,
        'builds': [
            {'chipFamily': "ESP32", 'parts': parts}
        ]
    }
    with open(
        os.path.join(
            settings.MEDIA_ROOT, 'esphome', '%s_manifest_%s.json' % (
                esp_device.name, esp_device.compiled_version
            )
        ), 'w'
    ) as f:
        f.write(json.dumps(manifest_data))

    try:
        # remove old manifest
        os.remove(os.path.join(
            settings.MEDIA_ROOT, 'esphome', '%s_manifest_%s.json' % (
                esp_device.name, old_version
            )
        ))
    except:
        pass

    esp_device.last_compile = timezone.now()
    esp_device.firmware_status = 'needs_update'
    esp_device.save()


@celery_app.task
def wifi_update(esp_device_id):
    esp_device = ESPDevice.objects.get(id=esp_device_id)
    if esp_device.firmware_status != 'needs_update':
        return
    esp_device.firmware_status = 'updating'
    esp_device.save()

    esphome_dir = os.path.join(settings.MEDIA_ROOT, 'esphome')
    logger = logging.getLogger(
        "ESP Device Logger [%d]" % esp_device.id
    )
    logger.propagate = False
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(message)s',
            "%m-%d %H:%M:%S"
        )
        formatter.converter = \
            lambda *args, **kwargs: timezone.localtime().timetuple()
        file_handler = RotatingFileHandler(
            get_log_file_path(esp_device), maxBytes=102400,  # 100KB
            backupCount=3, encoding='utf-8',
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    env = os.environ.copy()
    proc = subprocess.Popen(
        [
            'esphome', 'upload', '--device',
            '%s.local' % esp_device.name, '%s.yaml' % esp_device.name
        ],
        cwd=esphome_dir, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    with proc.stdout as stdout:
        for line in iter(stdout.readline, b''):
            logger.log(logging.INFO, line.decode().rstrip('\n'))

    status = proc.wait()
    if status:
        esp_device.firmware_status = 'needs_update'
        esp_device.save(update_fields=['firmware_status'])
        return

    esp_device.firmware_status = 'up_to_date'
    esp_device.save(update_fields=['firmware_status'])


