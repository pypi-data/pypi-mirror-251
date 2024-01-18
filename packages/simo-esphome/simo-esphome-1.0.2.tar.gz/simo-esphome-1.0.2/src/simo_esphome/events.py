from simo.core.events import ObjMqttAnnouncement


class ESPManagementEvent(ObjMqttAnnouncement):
    TOPIC = 'SIMO/esphome-management'