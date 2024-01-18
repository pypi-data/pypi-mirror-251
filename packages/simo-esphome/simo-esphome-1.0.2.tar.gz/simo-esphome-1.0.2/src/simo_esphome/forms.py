from django import forms
from dal import autocomplete
from dal import forward
from django.contrib import messages
from django.urls.base import get_script_prefix
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from simo.core.widgets import LogOutputWidget
from simo.core.forms import BaseComponentForm
from esphome.components.esp32.boards import ESP32_BOARD_PINS
from esphome.components.esp8266.boards import ESP8266_BOARD_PINS
from .models import ESPDevice
from .utils import (
    get_available_gpio_pins, get_gpio_pins_choices,
    get_last_wifi_ssid, get_last_wifi_password,
    build_config, validate_config, CLOCKED_NEOPIXELS
)


class ESPDeviceAdminForm(forms.ModelForm):
    wifi_password = forms.CharField(
        widget=forms.PasswordInput(
            render_value=True,
        )
    )
    log = forms.CharField(
        label="Build log", required=False, widget=forms.HiddenInput
    )
    dallas_hub = forms.TypedChoiceField(
        label="Enable Dallas Hub",
        choices=get_gpio_pins_choices, required=False, coerce=int,
        help_text=(
            "Will start Dallas Hub on corresponding pin for "
            "DS18b20 or similar 1-Wire temperature sensors, if specified."
        ),
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('id', 'esp_device'),
                forward.Const({'output': True}, 'filters')
            ]
        )
    )

    class Meta:
        model = ESPDevice
        fields = '__all__'
        widgets = {
            'board': autocomplete.ListSelect2(
                url='autocomplete-espboard',
                forward=['platform']
            )
        }

    class Media:
        js = [
            'third_party/esp-web-tools-7.1.0/install-button.js',
            'admin/js/esp_device_status_watchdog.js'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            prefix = get_script_prefix()
            if prefix == '/':
                prefix = ''
            self.fields['log'].widget = LogOutputWidget(
                prefix + '/ws/log/%d/%d/' % (
                    ContentType.objects.get_for_model(ESPDevice).id,
                    self.instance.id
                )
            )
            self.fields['id'] = forms.IntegerField(widget=forms.HiddenInput)
        else:
            self.initial['wifi_ssid'] = get_last_wifi_ssid()
            self.initial['wifi_password'] = get_last_wifi_password()


    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.pk:
            platform = cleaned_data['platform']
            if platform == 'esp32' \
            and cleaned_data['board'] not in ESP32_BOARD_PINS.keys():
                self.add_error(
                    'board', "This board is not of ESP32 platform."
                )
            elif platform == 'esp8266' \
            and cleaned_data['board'] not in ESP8266_BOARD_PINS.keys():
                self.add_error(
                    'board', "This board is not of ESP8266 platform."
                )
        return cleaned_data

    def clean_additional_yaml(self):
        if not self.cleaned_data['additional_yaml']:
            return self.cleaned_data['additional_yaml']
        instance = self.save(commit=False)
        validate_config(instance.get_current_config())
        return self.cleaned_data['additional_yaml']

    def clean_dallas_hub(self):
        dallas_hub = self.cleaned_data['dallas_hub']
        if not dallas_hub:
            return
        if self.instance.pk:
            selected = self.instance.dallas_hub
        else:
            selected = None
        free_pins = get_available_gpio_pins(
            self.instance, selected=selected
        )
        if dallas_hub not in free_pins:
            raise forms.ValidationError(
                'pin',
                "Sorry, but GPIO%d pin is occupied."
                % dallas_hub
            )
        input_pins = get_available_gpio_pins(
            self.instance, filters={'output': True},
            selected=selected
        )
        if dallas_hub not in input_pins:
            raise forms.ValidationError(
                'pin',
                "Sorry, but GPIO%d pin can not be used as input pin "
                % dallas_hub
            )
        return dallas_hub



class ESPComponentForm(BaseComponentForm):

    def clean_esp_device(self):
        org = self.instance.config.get('esp_device')
        if org and org != self.cleaned_data['esp_device'].id:
            raise forms.ValidationError(
                "Changing esp device after component is created "
                "would introduce a lot of confusion, therefore "
                "it is not allowed."
            )
        return self.cleaned_data['esp_device']

    def clean(self):
        self.cleaned_data = super().clean()

        if self.is_valid():
            # Validate full YAML config
            org_config = self.instance.config.copy()
            self.save(commit=False)
            base_data = self.cleaned_data['esp_device'].get_base_data()
            component_configs = []
            if self.instance.id:
                this_controller = self.instance.controller_cls(self.instance)
            else:
                this_controller = self.controller_cls(self.instance)
            for component in self.cleaned_data['esp_device'].components.all():
                if component.id == self.instance.id:
                    component_configs.append(this_controller._get_esp_config())
                else:
                    component_configs.append(component.controller._get_esp_config())

            if not self.instance.id:
                component_configs.append(this_controller._get_esp_config())

            new_config = build_config(
                base_data, component_configs,
                self.cleaned_data['esp_device'].additional_yaml
            )

            validate_config(new_config)

            for field_n in self.config_fields:
                if field_n == 'esp_device':
                    continue
                if org_config.get(field_n) != self.cleaned_data.get(field_n):
                    messages.warning(
                        self.request,
                        mark_safe("This will take full effect only after you "
                                  "<a href='%s' target=_blank>update %s firmware</a>." % (
                                      self.cleaned_data[
                                          'esp_device'].get_admin_url(),
                                      self.cleaned_data['esp_device'].name
                                  ))
                    )
                    break

        return self.cleaned_data


class ESPBinarySensorConfigForm(ESPComponentForm):
    esp_device = forms.ModelChoiceField(
        label="ESP Device", queryset=ESPDevice.objects.all()
    )
    pin = forms.TypedChoiceField(
        coerce=int, choices=get_gpio_pins_choices,
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'input': True}, 'filters')
            ]
        )
    )
    pull = forms.ChoiceField(
        choices=(
            ('HIGH', "HIGH"), ('LOW', "LOW"), ("FLOATING", "leave floating"),
        ),
        help_text="If you are not sure what is this all about, "
                  "you are most definitely want to pull this HIGH or LOW "
                  "but not leave it floating!"
    )
    inverse = forms.ChoiceField(
        choices=(('yes', "Yes"), ('no', "No")),
        help_text="Hint: Set pull HIGH and inverse to Yes, to get ON signal when "
                  "you deliver GND to the pin and OFF when you cut it out."
    )
    debounce = forms.IntegerField(
        min_value=0, max_value=1000 * 60 * 60, required=False, initial=100,
        help_text="Some sensors are unstable and quickly transition "
                  "between ON/OFF states when engaged. <br>"
                  "Set debounce value in milliseconds, to remediate this. "
                  "100ms offers a good starting point!"

    )

    def clean(self):
        super().clean()
        if 'pin' not in self.cleaned_data:
            return self.cleaned_data
        if self.instance.pk:
            selected = self.instance.config.get('pin')
        else:
            selected = None
        free_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], selected=selected
        )
        if self.cleaned_data['pin'] not in free_pins:
            self.add_error(
                'pin',
                "Sorry, but GPIO%d pin is occupied."
                % self.cleaned_data['pin']
            )
            return
        input_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], filters={'input': True},
            selected=selected
        )
        if self.cleaned_data['pin'] not in input_pins:
            self.add_error(
                'pin',
                "Sorry, but GPIO%d pin can not be used as input pin "
                % self.cleaned_data['pin']
            )
            return
        if self.cleaned_data.get('pull') != 'FLOATING':
            pins_available_for_pull = get_available_gpio_pins(
                self.cleaned_data['esp_device'], filters={'output': True},
                selected=selected
            )
            if self.cleaned_data['pin'] not in pins_available_for_pull:
                self.add_error(
                    'pin',
                    "Sorry, but GPIO%d pin does not have internal pull HIGH/LOW"
                    " resistance capability" % self.cleaned_data['pin']
                )
                return
        return self.cleaned_data


class ESPTouchSensorConfigForm(ESPComponentForm):
    esp_device = forms.ModelChoiceField(
        label="ESP Device", queryset=ESPDevice.objects.all()
    )
    pin = forms.TypedChoiceField(
        coerce=int, choices=get_gpio_pins_choices,
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'capacitive': True}, 'filters')
            ]
        )
    )
    threshold = forms.IntegerField(
        min_value=0, max_value=999999999, required=False, initial=1000,
        help_text="Used to detect touch events. "
                  "Smaller value means a higher sensitivity. "
                  "1000 offers good starting point."

    )
    inverse = forms.ChoiceField(choices=(('no', "No"), ('yes', "Yes")))

    def clean(self):
        super().clean()
        if 'pin' not in self.cleaned_data:
            return self.cleaned_data
        if self.instance.pk:
            selected = self.instance.config.get('pin')
        else:
            selected = None
        free_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], selected=selected
        )
        if self.cleaned_data['pin'] not in free_pins:
            self.add_error(
                'pin',
                "Sorry, but GPIO%d pin is occupied."
                % self.cleaned_data['pin']
            )
            return
        touch_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], filters={'capacitive': True},
            selected=selected
        )
        if self.cleaned_data['pin'] not in touch_pins:
            self.add_error(
                'pin',
                "Sorry, but GPIO%d pin can not be used as input pin "
                % self.cleaned_data['pin']
            )
            return
        return self.cleaned_data


class ESPSwitchConfigForm(ESPComponentForm):
    esp_device = forms.ModelChoiceField(
        label="ESP Device", queryset=ESPDevice.objects.all()
    )
    output_pin = forms.TypedChoiceField(
        coerce=int, choices=get_gpio_pins_choices,
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'output': True}, 'filters')
            ]
        )
    )
    engaged_action = forms.ChoiceField(
        choices=(('HIGH', "HIGH"), ('LOW', "LOW")),
    )
    control_pin = forms.TypedChoiceField(
        coerce=int, required=False, choices=get_gpio_pins_choices,
        help_text="Use this if you also want to wire up a wall switch",
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'input': True}, 'filters')
            ]
        )
    )
    control_pin_mode = forms.ChoiceField(
        required=False, choices=(
            ('HIGH', "Pull HIGH"), ('LOW', "Pull DOWN"),
            ('TOUCH', "Touch sensor"), ("FLOATING", "Leave floating"),
        ),
        help_text="If you are not sure what is this all about, "
                  "you are most definitely want to pull this HIGH or LOW "
                  "but not leave it floating!"
    )
    control_pin_inverse = forms.ChoiceField(
        required=False, choices=(('yes', "Yes"), ('no', "No")),
        help_text="Example: Set pull HIGH and inverse to Yes, to get ON signal when"
                  " you deliver GND to the control pin and OFF when you cut it out."
    )
    control_method = forms.ChoiceField(
        required=False, choices=(
            ('momentary', "Momentary"), ('toggle', "Toggle")
        ),
    )
    touch_threshold = forms.IntegerField(
        min_value=0, max_value=999999999, required=False, initial=1000,
        help_text="Used to detect touch events. "
                  "Smaller value means a higher sensitivity. "
                  "1000 offers good starting point. <br> "
                  "Used only when controll pin mode is set to Touch sensor."

    )
    auto_off = forms.IntegerField(
        required=False, min_value=1, max_value=1000000000,
        help_text="If provided, switch will be turned off after "
                  "given amount of milliseconds after every turn on event."
    )

    def clean(self):
        super().clean()
        if not self.cleaned_data.get('output_pin'):
            return self.cleaned_data
        if self.instance.pk:
            selected = self.instance.config.get('output_pin')
        else:
            selected = None
        free_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], selected=selected
        )
        if self.cleaned_data['output_pin'] not in free_pins:
            self.add_error(
                'output_pin',
                "Sorry, but GPIO%d pin is occupied."
                % self.cleaned_data['output_pin']
            )
            return
        output_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], filters={'output': True},
            selected=selected
        )
        if self.cleaned_data['output_pin'] not in output_pins:
            self.add_error(
                'output_pin',
                "Sorry, but GPIO%d pin can not be used as output pin "
                % self.cleaned_data['output_pin']
            )
            return
        if self.cleaned_data.get('control_pin'):
            if self.instance.pk:
                selected = self.instance.config.get('control_pin')
            else:
                selected = None
            free_pins = get_available_gpio_pins(
                self.cleaned_data['esp_device'], selected=selected
            )
            if self.cleaned_data['control_pin'] not in free_pins:
                self.add_error(
                    'control_pin',
                    "Sorry, but GPIO%d pin is occupied."
                    % self.cleaned_data['control_pin']
                )
                return

            filters = {'input': True}
            if self.cleaned_data.get('control_pin_mode') == 'TOUCH':
                filters['capacitive'] = True
            input_pins = get_available_gpio_pins(
                self.cleaned_data['esp_device'], filters=filters,
                selected=selected
            )
            if self.cleaned_data['control_pin'] not in input_pins:
                self.add_error(
                    'control_pin',
                    "Sorry, but GPIO%d pin can not be used as %s"
                    % (
                        self.cleaned_data['control_pin'],
                        "touch sensing pin"
                        if self.cleaned_data['control_pin_mode'] == 'TOUCH'
                        else "input pin"
                    )
                )
                return
        return self.cleaned_data


class ESPPWMOutputConfigForm(ESPComponentForm):
    esp_device = forms.ModelChoiceField(
        label="ESP Device", queryset=ESPDevice.objects.all()
    )
    output_pin = forms.TypedChoiceField(
        coerce=int, choices=get_gpio_pins_choices,
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'output': True}, 'filters')
            ]
        )
    )
    frequency = forms.IntegerField(
        min_value=30, max_value=100000, required=True, initial=1000,
        help_text="PWM signal frequency in Hz. "
                  "1000 Hz offers great performance in most use cases."

    )
    min = forms.FloatField(
        initial=0, help_text="Minimum component value."
    )
    max = forms.FloatField(
        initial=100, help_text="Maximum component value."
    )


    def clean(self):
        super().clean()
        if not self.cleaned_dataget('output_pin'):
            return self.cleaned_data
        if self.instance.pk:
            selected = self.instance.config.get('output_pin')
        else:
            self.cleaned_data['value_units'] = '%'
            selected = None
        free_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], selected=selected
        )
        if self.cleaned_data['output_pin'] not in free_pins:
            self.add_error(
                'output_pin',
                "Sorry, but GPIO%d pin is occupied."
                % self.cleaned_data['output_pin']
            )
            return
        output_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], filters={'output': True},
            selected=selected
        )
        if self.cleaned_data['output_pin'] not in output_pins:
            self.add_error(
                'output_pin',
                "Sorry, but GPIO%d pin can not be used as output pin "
                % self.cleaned_data['output_pin']
            )
            return
        return self.cleaned_data


class ACDimmerConfigForm(ESPComponentForm):
    esp_device = forms.ModelChoiceField(
        label="ESP Device", queryset=ESPDevice.objects.all()
    )
    gate_pin = forms.TypedChoiceField(
        coerce=int, choices=get_gpio_pins_choices,
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'output': True}, 'filters')
            ]
        )
    )
    zero_cross_pin = forms.TypedChoiceField(
        coerce=int, required=True, choices=get_gpio_pins_choices,
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'input': True, 'allow_occupied': True}, 'filters')
            ]
        )
    )
    method = forms.ChoiceField(
        required=False, choices=(
            ('leading pulse', "Leading Pulse (Default)"),
            ('leading', "Leading"),
            ('trailing', "Trailing (Mosfet dimmers only)")
        ),
    )
    init_with_half_cycle = forms.BooleanField(
        initial=False, required=False, help_text=(
            "Will send the first full half AC cycle. "
            "Try to use this for dimmable LED lights, "
            "it might help turning on at low brightness levels. "
            "On Halogen lamps it might show at initial flicker."
        )
    )
    min = forms.FloatField(
        initial=0, help_text="Minimum component value."
    )
    max = forms.FloatField(
        initial=100, help_text="Maximum component value."
    )

    def clean(self):
        super().clean()
        if not self.cleaned_data.get('gate_pin'):
            return self.cleaned_data
        if self.instance.pk:
            selected = self.instance.config.get('gate_pin')
        else:
            self.cleaned_data['value_units'] = '%'
            selected = None
        free_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], selected=selected
        )
        if self.cleaned_data['gate_pin'] not in free_pins:
            self.add_error(
                'output_pin',
                "Sorry, but GPIO%d pin is occupied."
                % self.cleaned_data['output_pin']
            )
            return
        output_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], filters={'output': True},
            selected=selected
        )
        if self.cleaned_data['gate_pin'] not in output_pins:
            self.add_error(
                'output_pin',
                "Sorry, but GPIO%d pin can not be used as output pin "
                % self.cleaned_data['output_pin']
            )
            return
        return self.cleaned_data


class DallasTemperatureSensorConfigForm(ESPComponentForm):
    esp_device = forms.ModelChoiceField(
        label="ESP Device", queryset=ESPDevice.objects.all()
    )
    address = forms.CharField(
        help_text="Connect your sensor to Dallas Hub pin and "
                  "inspect ESP device logs while connected via USB to get "
                  "your sensor addresses. ",
        widget=forms.TextInput(attrs={'placeholder': '0x31012036B570E528'})
    )
    temperature_units = forms.ChoiceField(
        label="Sensor temperature units",
        choices=(('C', "Celsius"), ('F', "Fahrenheit"))
    )


    def clean_esp_device(self):
        esp_device = self.cleaned_data['esp_device']
        if not esp_device.dallas_hub:
            raise forms.ValidationError(
                mark_safe("Please enable dallas hub in "
                "<a href='%s' target=_blank>%s advanced settings</a> first." %
                (esp_device.get_admin_url(), esp_device.name)
                )
            )
        return esp_device

    def clean_address(self):
        value = self.cleaned_data['address'].lower()
        base = 10
        if value.startswith("0x"):
            base = 16
        try:
            int(value, base)
        except ValueError:
            raise forms.ValidationError("Bad value")
        return value


class DHTClimateSensorConfigForm(ESPComponentForm):
    esp_device = forms.ModelChoiceField(
        label="ESP Device", queryset=ESPDevice.objects.all()
    )
    pin = forms.TypedChoiceField(
        coerce=int, choices=get_gpio_pins_choices,
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'output': True}, 'filters')
            ]
        )
    )
    model = forms.ChoiceField(
        required=True, choices=(
            ('AUTO_DETECT', "Auto Detect"),
            ('DHT11', "DHT11"),
            ('DHT22', "DHT22"),
            ('DHT22_TYPE2', "DHT22 TYPE2"),
            ('AM2302', "AM2302"),
            ('RHT03', "RHT03"),
            ('SI7021', "SI7021")
        ),
    )
    temperature_units = forms.ChoiceField(
        label="Sensor temperature units",
        choices=(('C', "Celsius"), ('F', "Fahrenheit"))
    )
    update_interval = forms.IntegerField(
        min_value=1, max_value=99999, initial=60
    )

    def clean(self):
        cleaned_data = super().clean()
        if not self.cleaned_data.get('pin'):
            return cleaned_data
        if self.instance.pk:
            selected = self.instance.config.get('pin')
        else:
            selected = None
        free_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], selected=selected
        )
        if self.cleaned_data['pin'] not in free_pins:
            self.add_error(
                'pin',
                "Sorry, but GPIO%d pin is occupied."
                % self.cleaned_data['pin']
            )
            return
        output_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], filters={'output': True},
            selected=selected
        )
        if self.cleaned_data['pin'] not in output_pins:
            self.add_error(
                'pin',
                "Sorry, but GPIO%d pin can not be used as output pin "
                % self.cleaned_data['pin']
            )
            return
        return cleaned_data


class AddressableRGBWConfigForm(ESPComponentForm):
    esp_device = forms.ModelChoiceField(
        label="ESP Device", queryset=ESPDevice.objects.all()
    )
    data_pin = forms.TypedChoiceField(
        coerce=int, choices=get_gpio_pins_choices,
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'output': True}, 'filters')
            ]
        )
    )
    clock_pin = forms.TypedChoiceField(
        coerce=int, choices=get_gpio_pins_choices, required=False,
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'output': True}, 'filters')
            ]
        )
    )
    variant = forms.ChoiceField(
        required=True, choices=(
            ('800KBPS', "800KBPS (generic option, recommended for chipsets without explicit support)"),
            ('400KBPS', "400KBPS"),
            ('WS2811', "WS2811"),
            ('WS2812X', "WS2812X"),
            ('WS2813', "WS2813"),
            ('SK6812', "SK6812"),
            ('TM1814', "TM1814"),
            ('TM1829', "TM1829"),
            ('TM1914', "TM1914"),
            ('APA106', "APA106"),
            ('LC8812', "LC8812"),
            ('WS2801', "WS2801"),
            ('DotStar', "DotStar"),
            ('LPD6803', "LPD6803"),
            ('LPD8806', "LPD8806"),
            ('P9813', "P9813"),
        ),
    )
    order = forms.ChoiceField(
        choices=[
            ('GRB', 'GRB (regular RGB)'), ('GRBW', 'GRBW (regular RGBW)'),
        ] + [(v, v) for v in (
            'GBR', 'BGR', 'RGB', 'BRG', 'GBWR', 'GBRW', 'GWBR',
            'GWRB', 'GRWB', 'BGWR', 'BGRW',  'WGBR', 'RGBW', 'WGRB', 'RGWB',
            'BWGR', 'BRGW', 'WBGR', 'RBGW', 'RBG', 'WRGB', 'RWGB', 'BWRG',
            'BRWG', 'WBRG', 'RBWG', 'WRBG', 'RWBG'
        )],
        help_text=(
            "Most manufacturers uses GRB(W) order for RGB(W) LED strips. <br>"
            "If your light shows different color than it should, most probably "
            "you have non regular order RGB(W) led light. "
            "Try changing this to something different in that case."
        )
    )
    num_leds = forms.IntegerField(
        label="Number of LED's",
        min_value=1, max_value=5000, required=True
    )


    def clean(self):
        cleaned_data = super().clean()
        if 'variant' not in cleaned_data:
            return cleaned_data


        if cleaned_data['variant'] in CLOCKED_NEOPIXELS:
            if not cleaned_data.get('clock_pin'):
                self.add_error(
                    'clock_pin',
                    "%s LED variant requires clock pin" % cleaned_data['variant']
                )
        else:
            if cleaned_data.get('clock_pin'):
                self.add_error(
                    'clock_pin',
                    "%s LED variant does not require clock pin" %
                    cleaned_data['variant']
                )

        if cleaned_data['variant'] in ('800KBPS', '400KBPS') \
        and not self.cleaned_data.get('order'):
            self.add_error(
                'order',
                "%s generic LED variant requires exact color order" %
                cleaned_data['variant']
            )

        self.instance.config['has_white'] = False
        if len(self.cleaned_data['order']) > 3:
            self.instance.config['has_white'] = True

        return cleaned_data


class ESPSGateConfigForm(ESPComponentForm):
    esp_device = forms.ModelChoiceField(
        label="ESP Device", queryset=ESPDevice.objects.all()
    )
    open_closed_sensor_pin = forms.TypedChoiceField(
        label='Open/Closed sensor pin',
        coerce=int, choices=get_gpio_pins_choices,
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'input': True}, 'filters')
            ]
        )
    )
    sensor_pull = forms.ChoiceField(
        choices=(
            ('HIGH', "HIGH"), ('LOW', "LOW"), ("FLOATING", "leave floating"),
        ),
        help_text="If you are not sure what is this all about, "
                  "you are most definitely want to pull this HIGH or LOW "
                  "but not leave it floating!"
    )
    sensor_inverse = forms.ChoiceField(
        choices=(('yes', "Yes"), ('no', "No")),
        help_text="Hint: Set pull HIGH and inverse to Yes, to get ON signal when "
                  "you deliver GND to the pin and OFF when you cut it out."
    )

    action_pin = forms.TypedChoiceField(
        coerce=int, choices=get_gpio_pins_choices,
        widget=autocomplete.ListSelect2(
            url='autocomplete-espboard-pins',
            forward=[
                forward.Self(),
                forward.Field('esp_device'),
                forward.Const({'output': True}, 'filters')
            ]
        )
    )
    engaged_action = forms.ChoiceField(
        choices=(('HIGH', "HIGH"), ('LOW', "LOW")),
    )
    action_method = forms.ChoiceField(
        required=True, choices=(
            ('click', "Click"),
            ('toggle', "Toggle"),
        ),
        help_text="Action switch method to initiate move/stop event on "
                  "your gate."
    )
    gate_open_duration = forms.IntegerField(
        label='Gate open duration', min_value=1, max_value=360,
        initial=30,
        help_text="Average time in seconds that takes for your gate to go "
                  "from fully closed to fully open."
    )

    def clean(self):
        super().clean()
        if self.instance.pk:
            selected = self.instance.config.get('open_closed_sensor_pin')
        else:
            selected = None
        free_pins = get_available_gpio_pins(
            self.cleaned_data['esp_device'], selected=selected
        )
        if self.cleaned_data.get('open_closed_sensor_pin'):
            if self.cleaned_data['open_closed_sensor_pin'] not in free_pins:
                self.add_error(
                    'open_closed_sensor_pin',
                    "Sorry, but GPIO%d pin is occupied."
                    % self.cleaned_data['pin']
                )
                return
            input_pins = get_available_gpio_pins(
                self.cleaned_data['esp_device'], filters={'input': True},
                selected=selected
            )
            if self.cleaned_data['open_closed_sensor_pin'] not in input_pins:
                self.add_error(
                    'open_closed_sensor_pin',
                    "Sorry, but GPIO%d pin can not be used as input pin "
                    % self.cleaned_data['open_closed_sensor_pin']
                )
                return
            if self.cleaned_data.get('sensor_pull') != 'FLOATING':
                pins_available_for_pull = get_available_gpio_pins(
                    self.cleaned_data['esp_device'], filters={'output': True},
                    selected=selected
                )
                if self.cleaned_data['open_closed_sensor_pin'] \
                    not in pins_available_for_pull:
                    self.add_error(
                        'open_closed_sensor_pin',
                        "Sorry, but GPIO%d pin does not have internal pull HIGH/LOW"
                        " resistance capability" % self.cleaned_data['pin']
                    )
                    return

        if self.cleaned_data.get('action_pin'):
            if self.cleaned_data['action_pin'] not in free_pins:
                self.add_error(
                    'action_pin',
                    "Sorry, but GPIO%d pin is occupied."
                    % self.cleaned_data['action_pin']
                )
                return
            output_pins = get_available_gpio_pins(
                self.cleaned_data['esp_device'], filters={'output': True},
                selected=selected
            )
            if self.cleaned_data['action_pin'] not in output_pins:
                self.add_error(
                    'action_pin',
                    "Sorry, but GPIO%d pin can not be used as output pin "
                    % self.cleaned_data['output_pin']
                )
                return

        return self.cleaned_data


class ESPSGenericConfigForm(ESPComponentForm):
    esp_device = forms.ModelChoiceField(
        label="ESP Device", queryset=ESPDevice.objects.all()
    )
    yaml_config = forms.CharField(
        label="YAML config", widget=forms.Textarea(),
        help_text='Use "name: simo_[id]" to bind esp entity to this component.'
    )
