import os
import yaml
from yaml import SafeDumper
import subprocess
from django import forms
from django.conf import settings
from django.utils.html import mark_safe
from ansi2html import Ansi2HTMLConverter
from pprint import pprint


# dump YAML None values to ''
SafeDumper.add_representer(
    type(None),
    lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', '')
)


GPIO_PIN_DEFAULTS = {
    'output': True, 'input': True, 'default_pull': 'FLOATING',
    'capacitive': False, 'note': ''
}

ESP32_GPIO_PINS = {
    0: {
        'capacitive': True,
        'default_pull': 'HIGH', 'note': "outputs PWM signal at boot"
    },
    1: {
        'input': False, 'note': "TX pin, debug output at boot"
    },
    2: {
        'capacitive': True, 'note': "on-board LED"
    },
    3: {
        'input': False, 'note': 'RX pin, HIGH at boot'
    },
    4: {
        'capacitive': True,
    },
    5: {
        'note': "outputs PWM signal at boot"
    },
    12: {
        'capacitive': True,
        'note': "boot fail if pulled HIGH"
    },
    13: {
        'capacitive': True,
    },
    14: {
        'capacitive': True,
        'note': "outputs PWM signal at boot",
    },
    15: {
        'capacitive': True,
        'note': "outputs PWM signal at boot"
    },
    16: {}, 17: {}, 18: {}, 19: {}, 21: {}, 22: {}, 23: {}, 25: {}, 26: {},
    27: {'capacitive': True},
    32: {'capacitive': True},
    33: {'capacitive': True},
    34: {'output': False},
    35: {'output': False},
    36: {'output': False},
    39: {'output': False},
}

ESP8266_GPIO_PINS = {
    0: {
        'note': 'connected to FLASH button, boot fails if pulled LOW',
        'default_pull': 'HIGH'
    },
    1: {
        'input': False,
        'note': 'TX pin, HIGH at boot, debug output at boot, boot fails if pulled LOW'
    },
    2: {
        'note': 'HIGH at boot, connected to on-board LED, boot fails if pulled LOW',
        'default_pull': 'HIGH'
    },
    3: {
        'output': False,
        'note': 'RX pin, HIGH at boot'
    },
    4: {}, 5: {}, 12: {}, 13: {}, 14: {},
    15: {
        'output': True,
        'note': 'pulled LOW, Boot fails if pulled HIGH',
        'default_pull': 'LOW'
    },
}

GPIO_PINS = {'esp32': {}, 'esp8266': {}}

CLOCKED_NEOPIXELS = ('WS2801', 'DotStar', 'LPD6803', 'LPD8806', 'P9813')

for no, data in ESP32_GPIO_PINS.items():
    GPIO_PINS['esp32'][no] = GPIO_PIN_DEFAULTS.copy()
    GPIO_PINS['esp32'][no].update(data)

for no, data in ESP8266_GPIO_PINS.items():
    GPIO_PINS['esp8266'][no] = GPIO_PIN_DEFAULTS.copy()
    GPIO_PINS['esp8266'][no].update(data)


def get_available_gpio_pins(esp_device=None, filters=None, selected=None):
    if not esp_device:
        return {no: GPIO_PIN_DEFAULTS for no in range(40)}
    if not filters:
        filters = {}
    pins = {}
    allow_occupied = filters.pop('allow_occupied', None)
    for key, data in GPIO_PINS.get(esp_device.platform, {}).items():
        if str(key) in esp_device.occupied_pins and not allow_occupied:
            if selected:
                if int(key) != int(selected):
                    continue
            else:
                continue
        skip = False
        for filter_param, filter_val in filters.items():
            if data[filter_param] != filter_val:
                skip = True
        if skip:
            continue
        pins[key] = data
    return pins


def get_gpio_pins_choices(esp_device=None, filters=None, selected=None):
    choices = []
    for key, data in get_available_gpio_pins(
        esp_device, filters, selected
    ).items():
        name = 'GPIO%d' % key
        if data.get('note'):
            name += ' | %s' % data['note']
        choices.append((key, name))
    return choices


def get_last_wifi_ssid():
    from .models import ESPDevice
    last_device = ESPDevice.objects.all().last()
    if last_device:
        return last_device.wifi_ssid

def get_last_wifi_password():
    from .models import ESPDevice
    last_device = ESPDevice.objects.all().last()
    if last_device:
        return last_device.wifi_password


def build_config(base_data, component_configs=None, additional_yaml=None):
    config_data = {
        'esphome': {
            'name': base_data['name'],
            'project': {
                'name': 'SIMO_io.esphome',
                'version': str(base_data['compiled_version'])
            }
        },
        base_data['platform']: {
            'board': base_data['board'],
            'framework': {'type': 'arduino'}
            if base_data['platform'] == 'esp32'
            else {'version': 'recommended'}
        },
        'logger': None,
        'api': {'password': base_data['api_secret']},
        'ota': {'password': base_data['api_secret']},
        'wifi': {
            'ssid': base_data['wifi_ssid'], 'password': base_data['wifi_password'],
            'ap': {'ssid': "%s fallback hotspot" % base_data['name'],
                   'password': base_data['api_secret']}
        },
        'captive_portal': None,
        'sensor': [
            {'platform': 'wifi_signal', 'name': 'wifi_signal'}
        ]
    }
    if base_data.get('dallas_hub'):
        config_data['dallas'] = [{'pin': base_data['dallas_hub']}]

    def append_config(config):
        if not isinstance(config, dict):
            config_data[config] = None
            return

        for key, val in config.items():
            if key in config_data:
                if isinstance(config_data[key], list):
                    if isinstance(config[key], list):
                        config_data[key].extend(config[key])
                    else:
                        config_data[key].append(config[key])
                else:
                    if isinstance(config[key], list):
                        config_data[key] = [config_data[key]] + config[key]
                    else:
                        config_data[key] = [config_data[key], config[key]]
            else:
                config_data[key] = config[key]

    if component_configs:
        for conf in component_configs:
            c_config = yaml.safe_load(conf)
            append_config(c_config)

    if additional_yaml:
        additional_config = yaml.safe_load(additional_yaml)
        append_config(additional_config)

    return yaml.safe_dump(config_data, indent=4, sort_keys=False)


def validate_config(config_yaml):
    esphome_dir = os.path.join(settings.MEDIA_ROOT, 'esphome')
    yaml_config_path = os.path.join(esphome_dir, 'test.yaml')
    if not os.path.exists(esphome_dir):
        os.makedirs(esphome_dir)
    with open(yaml_config_path, 'w') as yaml_config_f:
        yaml_config_f.write(config_yaml)
    proc = subprocess.Popen(
        ['esphome', 'config', 'test.yaml'],
        cwd=esphome_dir, env=os.environ.copy(),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        ansi_converter = Ansi2HTMLConverter()
        err = stdout.decode()
        err = mark_safe(ansi_converter.convert(err, full=False).replace('\n', '<br>'))
        raise forms.ValidationError(err)
