import sys
import logging
import threading
import json
import os
import aioesphomeapi
import asyncio
import time
import re
import paho.mqtt.client as mqtt
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.conf import settings
from simo.core.gateways import BaseGatewayHandler
from simo.core.forms import BaseGatewayForm
from simo.core.events import GatewayObjectCommand, get_event_obj
from simo.core.models import Component
from .events import ESPManagementEvent
from .models import ESPDevice


INFO_TO_COMMAND = {
    val: key + '_command' for key, val in
    aioesphomeapi.model.COMPONENT_TYPE_TO_INFO.items() if key in (
        'cover', 'fan', 'light', 'switch', 'climate', 'number', 'select',
        'siren', 'button'
    )
}


class ESPHomeGatewayHandler(BaseGatewayHandler):
    name = "ESPHome"
    config_form = BaseGatewayForm
    mqtt_client = None
    connections = {}
    component_to_esp = {}

    def run(self, exit):
        self.exit = exit
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.handle_devices())
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
        loop.close()
        ESPDevice.objects.all().update(connected=False, signal_strength=0)

    async def watch_device(self, esp_device):
        api = aioesphomeapi.APIClient(
            '%s.local' % esp_device.name, 6053, esp_device.api_secret
        )

        async def drop_connection():
            print("Connection lost to %s" % esp_device.name)
            self.connections.pop(esp_device.id, None)
            drop_components = []
            for comp_id, data in self.component_to_esp.items():
                if data['esp_device_id'] == esp_device.id:
                    drop_components.append(comp_id)
            for drop in drop_components:
                self.component_to_esp.pop(drop, None)

            def update_dead():
                for component in Component.objects.filter(
                    id__in=drop_components):
                    component.alive = False
                    component.save()

            await sync_to_async(update_dead, thread_sensitive=True)()

            try:
                await sync_to_async(
                    esp_device.refresh_from_db, thread_sensitive=True
                )()
            except ESPDevice.DoesNotExist:
                # device is deleted, quit this device watchdog.
                return

            esp_device.connected = False
            esp_device.signal_strength = 0
            await sync_to_async(esp_device.save, thread_sensitive=True)(
                update_fields=['connected', 'signal_strength']
            )
            # await asyncio.sleep(5)
            # print("Retry connection to %s" % esp_device.name)
            # await self.watch_device(esp_device)

        try:
            await api.connect(on_stop=drop_connection, login=True)
        except:
            print("Unable to connect to %s" % esp_device.name)
            esp_device.connected = False
            esp_device.signal_strength = 0
            await sync_to_async(esp_device.save, thread_sensitive=True)(
                update_fields=['connected', 'signal_strength']
            )
            return
            # await asyncio.sleep(5)
            # print("Retry connection to %s" % esp_device.name)
            # await self.watch_device(esp_device)

        self.connections[esp_device.id] = api

        device_info = await api.device_info()
        print("Connected to %s!" % device_info.name)

        esp_device.installed_version = device_info.project_version
        esp_device.connected = True
        await sync_to_async(esp_device.save, thread_sensitive=True)(
            update_fields=[
                'installed_version', 'connected', 'firmware_status'
            ]
        )
        entities, services = await api.list_entities_services()

        key_to_component = {}
        wifi_signal_key = 0
        for entity in entities:
            id_match = re.match(r'simo_(?P<id>[0-9]+).*', entity.object_id)
            if entity.object_id == 'wifi_signal':
                wifi_signal_key = entity.key

            elif id_match:
                try:
                    comp = await sync_to_async(
                        Component.objects.get, thread_sensitive=True
                    )(id=id_match.groups()[0])
                    key_to_component[entity.key] = {
                        'comp_id': comp.id, 'entity_info': entity
                    }
                    self.component_to_esp[comp.id] = {
                        'api': api, 'entity_info': entity,
                        'esp_device_id': esp_device.id,
                        'command': INFO_TO_COMMAND.get(type(entity))
                    }
                    comp.alive = True
                    await sync_to_async(comp.save, thread_sensitive=True)()
                except:
                    pass

        def on_state_change(state):
            if state.key == wifi_signal_key:
                esp_device.signal_strength = (state.state + 90) / 50 * 100
                if esp_device.signal_strength > 100:
                    esp_device.signal_strength = 100
                if esp_device.signal_strength < 0:
                    esp_device.signal_strength = 0
                esp_device.save(update_fields=['signal_strength'])
                return

            com_data = key_to_component.get(state.key)
            if not com_data:
                return

            try:
                component = Component.objects.get(id=com_data['comp_id'])
            except:
                return

            try:
                component.controller._receive_from_device(
                    {'state': state, 'info': com_data['entity_info']}
                )
            except Exception as e:
                logging.error(e, exc_info=True)

        await api.subscribe_states(on_state_change)


    async def handle_devices(self):

        def on_mqtt_connect(mqtt_client, userdata, flags, rc):
            command_event = GatewayObjectCommand(self.gateway_instance)
            mqtt_client.subscribe(command_event.get_topic())
            mqtt_client.subscribe(ESPManagementEvent.TOPIC)

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        self.mqtt_client.connect(host=settings.MQTT_HOST, port=settings.MQTT_PORT)
        self.mqtt_client.loop_start()

        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        esp_devices = await sync_to_async(
            list, thread_sensitive=True
        )(ESPDevice.objects.all())
        for esp_device in esp_devices:
            asyncio.create_task(self.watch_device(esp_device))

        counter = 0
        while not self.exit.is_set():
            await asyncio.sleep(1)
            if counter < 10:
                counter += 1
            else:
                counter = 0
                offline_devices = await sync_to_async(
                    list, thread_sensitive=True
                )(ESPDevice.objects.all().exclude(id__in=self.connections.keys()))
                for esp_device in offline_devices:
                    asyncio.create_task(self.watch_device(esp_device))


    def on_mqtt_message(self, client, userdata, msg):
        payload = json.loads(msg.payload)
        if msg.topic == ESPManagementEvent.TOPIC:
            esp_device = get_event_obj(payload, ESPDevice)
            if not esp_device:
                return
            if payload.get('event') == 'added':
                def run_watchdog_in_thread():
                    asyncio.run(self.watch_device(esp_device))
                threading.Thread(target=run_watchdog_in_thread, daemon=True).start()

        else:
            component = get_event_obj(payload, Component)
            ctrl = self.component_to_esp.get(component.id)
            if not ctrl:
                return

            if ctrl['command']:
                asyncio.run(
                    getattr(ctrl['api'], ctrl['command'])(
                        ctrl['entity_info'].key, **payload['send']
                    )
                )
