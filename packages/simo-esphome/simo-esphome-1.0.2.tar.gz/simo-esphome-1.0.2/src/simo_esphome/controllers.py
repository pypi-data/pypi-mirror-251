import yaml
from yaml import SafeDumper
from esphome.components.esp32.gpio import _translate_pin as _translate_esp32_pin
from esphome.components.esp8266.gpio import _translate_pin as _translate_esp8266_pin
from django.utils.translation import gettext_lazy as _
from simo.core.controllers import (
    ControllerBase, BinarySensor, NumericSensor, Switch, Dimmer, MultiSensor,
    RGBWLight
)
from simo.core.events import GatewayObjectCommand
from simo.core.app_widgets import BaseAppWidget
from simo.core.utils.helpers import heat_index
from simo.generic.controllers import Gate
from .gateways import ESPHomeGatewayHandler
from .forms import (
    ESPBinarySensorConfigForm, ESPTouchSensorConfigForm, ESPSwitchConfigForm,
    ESPSGenericConfigForm, ESPPWMOutputConfigForm, ACDimmerConfigForm,
    DallasTemperatureSensorConfigForm, DHTClimateSensorConfigForm,
    AddressableRGBWConfigForm, ESPSGateConfigForm
)
from .utils import CLOCKED_NEOPIXELS
from .models import ESPDevice
from simo.conf import dynamic_settings


# dump YAML None values to ''
SafeDumper.add_representer(
    type(None),
    lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', '')
)


class ESPBinarySensor(BinarySensor):
    gateway_class = ESPHomeGatewayHandler
    config_form = ESPBinarySensorConfigForm

    def _get_occupied_pins(self):
        return [self.component.config['pin']]

    def _get_esp_config(self):
        comp_config = self.component.config
        data = {
            'binary_sensor': [{
                'name': 'simo_%s' % str(self.component.id),
                'id': 'simo_%s' % str(self.component.id),
                'platform': 'gpio', 'pin': {
                    'number': comp_config['pin'],
                    'mode': {
                        'input': True
                    }
                },
                'filters': []
            }]
        }
        if comp_config['inverse'] == 'yes':
            data['binary_sensor'][0]['filters'].append({'invert': None})
        if comp_config['pull'] == 'HIGH':
            data['binary_sensor'][0]['pin']['mode']['pullup'] = True
        elif comp_config['pull'] == 'LOW':
            data['binary_sensor'][0]['pin']['mode']['pulldown'] = True
        if comp_config['debounce']:
            data['binary_sensor'][0]['filters'].extend([
                {'delayed_on': '%dms' % comp_config['debounce']},
                {'delayed_off': '%dms' % comp_config['debounce']}
            ])
        return yaml.safe_dump(data, indent=4, sort_keys=False)

    def _receive_from_device(self, data):
        self.set(data['state'].state)


class ESPTouchSensor(BinarySensor):
    name = _("Touch sensor")
    gateway_class = ESPHomeGatewayHandler
    config_form = ESPTouchSensorConfigForm

    def _get_occupied_pins(self):
        return [self.component.config['pin']]

    def _get_esp_config(self):
        comp_config = self.component.config
        data = {
            'esp32_touch': {'setup_mode': False},
            'binary_sensor': [{
                'name': 'simo_%s' % str(self.component.id),
                'id': 'simo_%s' % str(self.component.id),
                'platform': 'esp32_touch',
                'pin': comp_config['pin'],
                'threshold': comp_config['threshold']
            }]
        }
        if comp_config.get('inverse') == 'yes':
            data['binary_sensor'][0]['filters'] = [{'invert': None}]
        return yaml.safe_dump(data, indent=4, sort_keys=False)

    def _receive_from_device(self, state, info):
        self.set(state.state)


class ESPSwitch(Switch):
    gateway_class = ESPHomeGatewayHandler
    config_form = ESPSwitchConfigForm

    def _get_occupied_pins(self):
        pins = [self.component.config['output_pin']]
        if self.component.config.get('control_pin'):
            pins.append(self.component.config['control_pin'])
        return pins

    def _get_esp_config(self):
        comp_config = self.component.config
        data = {
            'switch': [{
                'name': 'simo_%s' % str(self.component.id),
                'id': 'simo_%s' % str(self.component.id),
                'platform': 'gpio', 'pin': {
                    'number': comp_config['output_pin'],
                }
            }]
        }
        if comp_config['engaged_action'] == 'LOW':
            data['switch'][0]['pin']['inverted'] = True
        if comp_config['auto_off']:
            data['switch'][0]['on_turn_on'] = [
                {'delay': '%dms' % comp_config['auto_off']},
                {'switch.turn_off': 'simo_%s' % str(self.component.id)}
            ]
        if comp_config.get('control_pin'):

            data['binary_sensor'] = [{
                'id': 'c_control_%s' % str(self.component.id),
                'platform': 'gpio', 'pin': {
                    'number': comp_config['control_pin'],
                    'mode': {'input': True}
                },
                'filters': [
                    {'delayed_on': '50ms'},
                    {'delayed_off': '50ms'}
                ]
            }]
            if comp_config.get('control_pin_mode') == 'TOUCH':
                data['esp32_touch'] = {'setup_mode': False}
                data['binary_sensor'][0]['platform'] = 'esp32_touch'
                data['binary_sensor'][0]['pin'] = comp_config['control_pin']
                data['binary_sensor'][0]['threshold'] = comp_config.get(
                    'touch_threshold', 1000
                )

            if comp_config['control_pin_inverse'] == 'yes':
                data['binary_sensor'][0]['filters'].append({'invert': None})

            if comp_config['control_pin_mode'] == 'HIGH':
                data['binary_sensor'][0]['pin']['mode']['pullup'] = True
            elif comp_config['control_pin_mode'] == 'LOW':
                data['binary_sensor'][0]['pin']['mode']['pulldown'] = True

            if comp_config['control_method'] == 'momentary':
                data['binary_sensor'][0]['on_click'] = {
                    'min_length': '50ms',
                    'max_length': "3000ms",
                    'then': [{'switch.toggle': 'simo_%s' % str(self.component.id)}]
                }
            else:
                data['binary_sensor'][0]['on_press'] = {
                    'then': [{'switch.toggle': 'simo_%s' % str(self.component.id)}]
                }
                data['binary_sensor'][0]['on_release'] = {
                    'then': [
                        {'switch.toggle': 'simo_%s' % str(self.component.id)}]
                }
        return yaml.safe_dump(data, indent=4, sort_keys=False)

    def _send_to_device(self, value):
        GatewayObjectCommand(
            self.component.gateway,
            self.component, send={'state': value}
        ).publish()

    def _receive_from_device(self, data):
        self.set(data['state'].state)


class ESPPWMOutput(Dimmer):
    name = _('PWM output')
    gateway_class = ESPHomeGatewayHandler
    config_form = ESPPWMOutputConfigForm

    def _get_occupied_pins(self):
        pins = [self.component.config['output_pin']]
        return pins

    def _get_esp_config(self):
        comp_config = self.component.config
        esp_device = ESPDevice.objects.get(id=comp_config.get('esp_device'))
        platform = 'ledc'
        if esp_device.platform == 'esp8266':
            platform = 'esp8266_pwm'
        data = {
            'light': [{
                'platform': 'monochromatic',
                'name': 'simo_%s' % str(self.component.id),
                'id': 'simo_%s' % str(self.component.id),
                'output': 'output_simo_%s' % str(self.component.id),
            }],
            'output': [{
                'platform': platform,
                'id': 'output_simo_%s' % str(self.component.id),
                'pin': comp_config['output_pin'],
                'frequency': comp_config['frequency']
            }]
        }
        return yaml.safe_dump(data, indent=4, sort_keys=False)

    def _send_to_device(self, value):
        conf = self.component.config
        com_amplitude = conf.get('max', 1.0) - conf.get('min', 0.0)
        float_value = com_amplitude * value - conf.get('min', 0.0)
        GatewayObjectCommand(
            self.component.gateway, self.component,
            send={'state': True, 'brightness': float_value}
        ).publish()

    def _receive_from_device(self, data):
        self.set(data['state'].brightness)


class ACDimmer(Dimmer):
    name = _("AC Dimmer")
    gateway_class = ESPHomeGatewayHandler
    config_form = ACDimmerConfigForm

    def _get_occupied_pins(self):
        pins = [
            self.component.config['gate_pin'],
            self.component.config['zero_cross_pin']
        ]
        return pins

    def _get_esp_config(self):
        config = self.component.config
        data = {
            'output': [{
                'platform': 'ac_dimmer',
                'id': 'output_simo_%s' % str(self.component.id),
                'gate_pin': config['gate_pin'],
                'zero_cross_pin': {
                    'number': config['zero_cross_pin'],
                    'mode': {'input': True},
                    'inverted': 'yes'
                }
            }],
            'light': [{
                'platform': 'monochromatic',
                'output': 'output_simo_%s' % str(self.component.id),
                'name': 'simo_%s' % str(self.component.id),
                'id': 'simo_%s' % str(self.component.id)
            }]
        }
        return yaml.safe_dump(data, indent=4, sort_keys=False)

    def _send_to_device(self, value):
        conf = self.component.config
        com_amplitude = conf.get('max', 1.0) - conf.get('min', 0.0)
        float_value = com_amplitude * value - conf.get('min', 0.0)
        GatewayObjectCommand(
            self.component.gateway, self.component,
            send={'state': True, 'brightness': float_value}
        ).publish()

    def _receive_from_device(self, data):
        self.set(data['state'].brightness)


class DallasTemperatureSensor(NumericSensor):
    name = _("Dallas Temperature Sensor")
    gateway_class = ESPHomeGatewayHandler
    config_form = DallasTemperatureSensorConfigForm
    sys_temp_units = 'C'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if dynamic_settings['core__units_of_measure'] == 'imperial':
            self.sys_temp_units = 'F'

    def _get_occupied_pins(self):
        return []

    def _get_esp_config(self):
        comp_config = self.component.config
        data = {
            'sensor': [{
                'name': 'simo_%s' % str(self.component.id),
                'id': 'simo_%s' % str(self.component.id),
                'platform': 'dallas',
                'address': comp_config.get('address', 60),
            }]
        }
        return yaml.safe_dump(data, indent=4, sort_keys=False)

    def _receive_from_device(self, data):
        val = data['state'].state
        if self.component.config.get('temperature_units') == 'C':
            if self.sys_temp_units == 'F':
                val = round((val * 9 / 5) + 32, 1)
        else:
            if self.sys_temp_units == 'C':
                val = round((val - 32) * 5 / 9, 1)
        self.set(val)


class DHTClimateSensor(MultiSensor):
    name = _("DHT Climate Sensor")
    gateway_class = ESPHomeGatewayHandler
    config_form = DHTClimateSensorConfigForm
    sys_temp_units = 'C'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if dynamic_settings['core__units_of_measure'] == 'imperial':
            self.sys_temp_units = 'F'

    @property
    def default_value(self):
        return [
            ['temperature', 0, self.sys_temp_units],
            ['humidity', 20, '%'],
            ['real_feel', 0, self.sys_temp_units]
        ]

    def _get_occupied_pins(self):
        return [self.component.config['pin']]

    def _get_esp_config(self):
        comp_config = self.component.config
        data = {
            'sensor': [{
                'platform': 'dht', 'pin': comp_config['pin'],
                'update_interval': '%ds' % comp_config['update_interval'],
                'temperature': {
                    'name': 'simo_%s_temp' % str(self.component.id),
                    'id': 'simo_%s_temp' % str(self.component.id),
                },
                'humidity': {
                    'name': 'simo_%s_hum' % str(self.component.id),
                    'id': 'simo_%s_hum' % str(self.component.id),
                }
            }]
        }
        return yaml.safe_dump(data, indent=4, sort_keys=False)

    def _receive_from_device(self, data):
        new_val = self.component.value.copy()
        if data['info'].device_class == 'temperature':
            new_val[0] = [
                'temperature', round(data['state'].state, 1),
                self.sys_temp_units
            ]
        elif data['info'].device_class == 'humidity':
            new_val[1] = ['humidity', round(data['state'].state, 1), '%']

        if self.component.config.get('temperature_units') == 'C':
            if self.sys_temp_units == 'F':
                new_val[0][1] = round((new_val[0][1] * 9 / 5) + 32, 1)
        else:
            if self.sys_temp_units == 'C':
                new_val[0][1] = round((new_val[0][1] - 32) * 5 / 9, 1)

        real_feel = heat_index(
            new_val[0][1], new_val[1][1], self.sys_temp_units == 'F'
        )
        new_val[2] = ['real_feel', real_feel, self.sys_temp_units]
        self.set(new_val)


class AddressableRGBW(RGBWLight):
    name = _("Addressable RGB(W) light")
    gateway_class = ESPHomeGatewayHandler
    config_form = AddressableRGBWConfigForm

    def _get_occupied_pins(self):
        pins = [self.component.config['data_pin']]
        if self.component.config.get('clock_pin'):
            pins.append(self.component.config['clock_pin'])
        return pins

    def _get_esp_config(self):
        comp_config = self.component.config
        data = {
            'light': [{
                'platform': 'neopixelbus',
                'variant': comp_config['variant'],
                'num_leds': comp_config['num_leds'],
                'type': comp_config['order'],
                'name': 'simo_%s' % str(self.component.id),
                'id': 'simo_%s' % str(self.component.id),
            }]
        }
        if comp_config['variant'] in CLOCKED_NEOPIXELS:
            data['light'][0]['data_pin'] = comp_config['data_pin']
            data['light'][0]['clock_pin'] = comp_config['clock_pin']
        else:
            data['light'][0]['pin'] = comp_config['data_pin']
        return yaml.safe_dump(data, indent=4, sort_keys=False)

    def _receive_from_device(self, data):
        if not data['state'].state:
            val = '#000000'
            if self.component.config.get('has_white'):
                val += '00'
        else:
            val = ''.join([
                '#',
                str(hex(int(round(data['state'].red * 255, 0))))[2:],
                str(hex(int(round(data['state'].green * 255, 0))))[2:],
                str(hex(int(round(data['state'].blue * 255, 0))))[2:]
            ])
            if self.component.config.get('has_white'):
                val += hex(int(round(data['state'].white * 255, 0)))[2:]
        self.set(val)

    def _send_to_device(self, value):
        send_data = {
            'state': True,
            'rgb': [
                float(int('0x' + value[1:3], base=16)) / 255.0,
                float(int('0x' + value[3:5], base=16)) / 255.0,
                float(int('0x' + value[5:7], base=16)) / 255.0
            ]
        }
        if self.component.config.get('has_white'):
            send_data['white'] = float(int('0x' + value[7:9], base=16)) / 255.0
            if value == '#00000000':
                send_data['state'] = False
        else:
            if value == '#000000':
                send_data['state'] = False
        GatewayObjectCommand(
            self.component.gateway, self.component, send=send_data
        ).publish()


class ESPGate(Gate):
    gateway_class = ESPHomeGatewayHandler
    config_form = ESPSGateConfigForm

    def _get_occupied_pins(self):
        return [
            self.component.config['open_closed_sensor_pin'],
            self.component.config['action_pin']
        ]

    def _get_esp_config(self):
        comp_config = self.component.config
        data = {
            'binary_sensor': [{
                'name': 'simo_%s_sensor' % str(self.component.id),
                'id': 'simo_%s_sensor' % str(self.component.id),
                'platform': 'gpio', 'pin': {
                    'number': comp_config['open_closed_sensor_pin'],
                    'mode': {
                        'input': True
                    }
                },
                'filters': [
                    {'delayed_on': '100ms'},
                    {'delayed_off': '100ms'}
                ]
            }],
            'switch': [{
                'name': 'simo_%s_switch' % str(self.component.id),
                'id': 'simo_%s_switch' % str(self.component.id),
                'platform': 'gpio', 'pin': {
                    'number': comp_config['action_pin'],
                }
            }]
        }
        if comp_config['sensor_inverse'] == 'yes':
            data['binary_sensor'][0]['filters'].append({'invert': None})
        if comp_config['sensor_pull'] == 'HIGH':
            data['binary_sensor'][0]['pin']['mode']['pullup'] = True
        elif comp_config['sensor_pull'] == 'LOW':
            data['binary_sensor'][0]['pin']['mode']['pulldown'] = True
        if comp_config['engaged_action'] == 'LOW':
            data['switch'][0]['pin']['inverted'] = True
        if comp_config['action_method'] == 'click':
            data['switch'][0]['on_turn_on'] = [
                {'delay': '500ms'},
                {'switch.turn_off': 'simo_%s_switch' % str(self.component.id)}
            ]

        return yaml.safe_dump(data, indent=4, sort_keys=False)

    def _send_to_device(self, value):
        self.component.refresh_from_db()
        if self.component.config.get('action_method') == 'click':
            GatewayObjectCommand(
                self.component.gateway, self.component, send={'state': True}
            ).publish()
        else:
            if self.component.value.startswith('open'):
                GatewayObjectCommand(
                    self.component.gateway, self.component, send={'state': False}
                ).publish()
            else:
                GatewayObjectCommand(
                    self.component.gateway, self.component, send={'state': True}
                ).publish()

    def _receive_from_device(self, data):
        if data['info'].object_id == 'simo_%s_switch' % str(self.component.id):
            if self.component.config.get('action_method') == 'toggle':
                self._set_on_the_move()
            else:
                if not data['state'].state: # click release:
                    # Button released
                    # set stopped position if it was moving, or set moving if not.
                    if self.component.value.endswith('moving'):
                        if self.component.config.get('sensor_value'):
                            self.component.set('open')
                        else:
                            self.component.set('closed')
                    else:
                        self._set_on_the_move()
        elif data['info'].object_id == 'simo_%s_sensor' % str(self.component.id):
            self.component.config['sensor_value'] = data['state'].state
            self.component.save(update_fields=['config'])
            # If sensor goes from False to True, while gate is moving
            # it usually means that gate just started the move and must stay in the move
            # user defined amount of seconds to represent actual gate movement.
            # Open state therefore is reached only after user defined duration.
            # If it was not in the move, then it simply means that it was
            # opened in some other way and we set it to open immediately.
            if data['state'].state:
                print("SET OPEN")
                if self.component.value.endswith('moving'):
                    self.set('open_moving')
                else:
                    self.set('open')
            # if binary sensor detects gate close event
            # we set gate value to closed immediately as it means that
            # gate is now truly closed and no longer moving.
            else:
                print("SET CLOSED")
                self.set('closed')





class ESPGeneric(ControllerBase):
    name = _("Generic ESP device component")
    base_type = 'esp-entity'
    gateway_class = ESPHomeGatewayHandler
    config_form = ESPSGenericConfigForm
    app_widget = BaseAppWidget
    default_value = {}

    def _validate_val(self, value, occasion=None):
        # we have no idea on how one might utilize this component type
        # therefore we can't provide proper value validation.
        return value

    def _get_occupied_pins(self):
        def traverse_config(config):
            pins = []
            if isinstance(config, dict):
                for key, val in config.items():
                    if key.endswith('pin'):
                        if isinstance(val, dict):
                            pin = val.get('number')
                            if pin:
                                pins.append(pin)
                        else:
                            pins.append(val)
                    elif isinstance(val, dict) or isinstance(val, list):
                        pins.extend(traverse_config(val))
            elif isinstance(config, list):
                for item in config:
                    if isinstance(item, dict):
                        pins.extend(traverse_config(item))
            return pins
        occupied_pins = traverse_config(yaml.safe_load(self._get_esp_config()))
        gpio_pins = set()
        translator = _translate_esp32_pin
        try:
            if ESPDevice.objects.get(
                id=self.component.conf.get('esp_device')
            ).platform == 'esp8266':
                translator = _translate_esp8266_pin
        except:
            pass
        for pin in occupied_pins:
            try:
                gpio_pins.add(translator(pin))
            except:
                pass
        return list(gpio_pins)

    def _get_esp_config(self):
        return self.component.config.get('yaml_config', '')

    def _send_to_device(self, value):
        from simo.core.events import GatewayObjectCommand
        if not isinstance(value, dict):
            value = {'state': value}
        GatewayObjectCommand(
            self.component.gateway, self.component, send=value
        ).publish()

    def _receive_from_device(self, data):
        self.set(data['state'].state)
