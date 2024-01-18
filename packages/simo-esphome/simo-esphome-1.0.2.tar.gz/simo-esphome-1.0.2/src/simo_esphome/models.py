import os
import shutil
from django.db import transaction
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.conf import settings
from simo.core.models import Gateway, Component
from simo.core.utils.mixins import SimoAdminMixin
from simo.core.utils.helpers import get_random_string
from esphome.components.esp32.boards import ESP32_BOARD_PINS
from esphome.components.esp8266.boards import ESP8266_BOARD_PINS
from .events import ESPManagementEvent
from .utils import get_last_wifi_ssid, get_last_wifi_password, build_config




class ESPDevice(models.Model, SimoAdminMixin):
    name = models.SlugField(
        max_length=40, db_index=True, unique=True
    )
    api_secret = models.CharField(
        max_length=100, default=get_random_string, editable=False,
        help_text="Used for communications encryption and as hotspot password "
                  "in fallback mode when device is unable to connect to your WiFi."
    )
    platform = models.CharField(
        default='esp32', max_length=50,
        choices=(('esp32', 'ESP32'), ('esp8266', 'ESP8266'))
    )
    board = models.CharField(
        default='esp32dev', max_length=100,
        help_text="* Use platform:ESP8266 board:esp01_1m for Sonoff devices.",
        choices=[
            (k, k) for k in ESP32_BOARD_PINS.keys()
        ] + [
            (k, k) for k in ESP8266_BOARD_PINS.keys()
        ]
    )
    wifi_ssid = models.CharField(
        max_length=100, default=get_last_wifi_ssid
    )
    wifi_password = models.CharField(
        max_length=100, default=get_last_wifi_password
    )
    dallas_hub = models.PositiveIntegerField(
        "Enable dallas hub", null=True, blank=True,
    )
    additional_yaml = models.TextField(blank=True, null=True)
    connected = models.BooleanField(
        "WiFi connection", default=False, db_index=True
    )
    signal_strength = models.PositiveIntegerField(
        null=True, editable=False, help_text="Signal strength in %"
    )
    installed_version = models.CharField(
        max_length=100, editable=False, blank=True, null=True
    )
    compiled_version = models.CharField(
        max_length=100, editable=False, blank=True, null=True
    )
    compiling = models.BooleanField(default=False, editable=False)
    firmware_status = models.CharField(
        'firmware',
        max_length=50, default='out_of_date', db_index=True, choices=(
            ('up_to_date', "Up to date"), ('out_of_date', "Out of date!"),
            ('compiling', "Compiling..."), ('needs_update', "Needs update!"),
            ("updating", "Updating...")
        )
    )

    components = models.ManyToManyField(Component, editable=False)
    occupied_pins = models.JSONField(default=dict, blank=True)

    last_compile = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta:
        verbose_name = 'ESP Device'
        verbose_name_plural = 'ESP Devices'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower().replace('_', '-')
        if self.pk and self.installed_version == self.compiled_version \
        and self.firmware_status in ('needs_update', 'updating'):
            self.firmware_status = 'up_to_date'
        if self.id:
            org = ESPDevice.objects.get(id=self.id)
            if org.name != self.name:
                org.clean_build_files()
            if org.additional_yaml != self.additional_yaml:
                self.firmware_status = 'out_of_date'
            if org.dallas_hub != self.dallas_hub:
                self.rebuild_occupied_pins()
        return super().save(*args, **kwargs)

    def get_base_data(self):
        base_data = {}
        for field_name in (
            'name', 'compiled_version', 'platform', 'board', 'api_secret',
            'wifi_ssid', 'wifi_password', 'dallas_hub'
        ):
            base_data[field_name] = getattr(self, field_name)
        return base_data

    def get_component_configs(self):
        component_configs = []
        if self.id:
            for component in self.components.all():
                component_configs.append(component.controller._get_esp_config())
        return component_configs

    def get_current_config(self):
        return build_config(
            self.get_base_data(), self.get_component_configs(),
            self.additional_yaml
        )

    def rebuild_occupied_pins(self):
        self.occupied_pins = {}
        if self.dallas_hub:
            self.occupied_pins[self.dallas_hub] = 'dallas'
        for component in self.components.all():
            try:
                pins = component.controller._get_occupied_pins()
            except:
                pins = []
            for pin in pins:
                self.occupied_pins[pin] = component.id

    def clean_build_files(self):
        root = os.path.join(settings.MEDIA_ROOT, 'esphome')
        remove_paths = [
            os.path.join(root, '%s.yaml' % self.name),
            os.path.join(root, '%s_manifest.json' % self.name),
            os.path.join(root, '.esphome', '%s.yaml.json' % self.name),
            os.path.join(root, '.esphome', 'idedata', '%s.json' % self.name),
            os.path.join(root, '.esphome', 'build', self.name),
            os.path.join(root, '%s_build_%s' % (self.name, self.compiled_version)),
        ]
        for path in remove_paths:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except:
                pass


@receiver(post_save, sender=ESPDevice)
def post_device_save(sender, instance, created=None, *args, **kwargs):
    if created:
        # Create ESPHome gateway automatically if it is not yet created.
        from .gateways import ESPHomeGatewayHandler
        Gateway.objects.get_or_create(type=ESPHomeGatewayHandler.uid)

        def post_create():
            print("FIRE CREATE EVENT!")
            ESPManagementEvent(instance, 'added').publish()
        transaction.on_commit(post_create)


@receiver(pre_delete, sender=ESPDevice)
def post_device_delete(sender, instance, *args, **kwargs):
    instance.clean_build_files()
    instance.components.all().delete()


@receiver(pre_delete, sender=Component)
def post_component_delete(sender, instance, *args, **kwargs):
    if not instance.controller_uid.startswith('simo_esphome'):
        return
    for esp_device in ESPDevice.objects.filter(components=instance):
        esp_device.components.remove(instance)
        esp_device.rebuild_occupied_pins()
        esp_device.save()


@receiver(post_save, sender=Component)
def post_component_save(sender, instance, created=None, *args, **kwargs):
    from .gateways import ESPHomeGatewayHandler
    if instance.gateway.type != ESPHomeGatewayHandler.uid:
        return
    if not created and 'config' not in instance.get_dirty_fields():
        return
    try:
        esp_device = ESPDevice.objects.get(id=instance.config.get('esp_device'))
    except ESPDevice.DoesNotExist:
        return
    else:
        esp_device.components.add(instance)
        for esp_device in ESPDevice.objects.filter(components=instance):
            esp_device.rebuild_occupied_pins()
            esp_device.firmware_status = 'out_of_date'
            esp_device.save()
