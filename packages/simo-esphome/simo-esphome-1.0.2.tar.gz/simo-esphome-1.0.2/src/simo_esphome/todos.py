from .models import ESPDevice


def update_esp_devices():
    todos = []
    for device in ESPDevice.objects.all().exclude(
        firmware_status__in=('updating', 'up_to_date')
    ):
        todos.append({
            'icon': 'fas fa-microchip',
            'label': "%s (ESP device) needs firmware update!" % device.name,
            'link': device.get_admin_url()
        })
    return todos
