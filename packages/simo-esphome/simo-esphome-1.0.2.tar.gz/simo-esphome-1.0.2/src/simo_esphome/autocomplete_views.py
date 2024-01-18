from dal import autocomplete
from esphome.components.esp32.boards import ESP32_BOARD_PINS
from esphome.components.esp8266.boards import ESP8266_BOARD_PINS
from .models import ESPDevice
from .utils import get_gpio_pins_choices


class BoardSelectAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        if not self.request.user.is_staff:
            return []

        if self.forwarded.get("platform") == 'esp32':
            return [(k, k) for k in ESP32_BOARD_PINS.keys()]
        elif self.forwarded.get("platform") == 'esp8266':
            return [(k, k) for k in ESP8266_BOARD_PINS.keys()]

        return []


class PinsSelectAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        if not self.request.user.is_staff:
            return []

        try:
            esp_device = ESPDevice.objects.get(
                pk=self.forwarded.get("esp_device")
            )
        except:
            return []

        return get_gpio_pins_choices(
            esp_device, self.forwarded.get('filters'),
            self.forwarded.get('self')
        )
