from django.template.loader import render_to_string
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import ESPDevice
from .tasks import rebuild_firmware, wifi_update


def firmware_status_view(request, id):
    if not request.user.is_authenticated:
        raise Http404()
    esp_device = get_object_or_404(ESPDevice, id=id)
    data = {'connected': render_to_string(
        'admin/esp_connection_display.html', {'obj': esp_device}
    )}

    if esp_device.firmware_status == 'out_of_date':
        if esp_device.installed_version:
            data['firmware'] = (
                '<span style="color: red">Out of date.</span>&nbsp;&nbsp;&nbsp;'
                '<button class="button default" id="rebuild-firmware" type="button">'
                '<i class="fas fa-sync"></i> Rebuild!</button>'
            )
        else:
            data['firmware'] = (
                '<button class="button default" id="rebuild-firmware" type="button">'
                '<i class="fas fa-play"></i> Build</button>'
            )

    elif esp_device.firmware_status == 'needs_update':
        if esp_device.installed_version:
            data['firmware'] = '<span style="color: red">Needs update!</span>'
        else:
            data['firmware'] = '<span style="color: red">Ready for install!</span>'
        if esp_device.connected:
            data['firmware'] += (
                ' <br><br><button class="button default" id="wifi-update" type="button">'
                'Update via WiFi</button>'
            )

    elif esp_device.firmware_status in ('compiling', 'updating'):
        data['firmware'] = '<i class="fas fa-spinner fa-spin"></i> %s' % \
                           esp_device.get_firmware_status_display()
    else:
        data['firmware'] = esp_device.get_firmware_status_display()


    if esp_device.firmware_status in ('needs_update', 'updating') \
    and esp_device.connected:
        warn = (
            "WARNING! Make sure ESP device is in power while updating "
            "over the WiFi. If power loss occurs, you might only be able to "
            "update it via USB."
        )
        data['firmware'] += '<br><br><span class="help">%s</span>' % warn

    if esp_device.firmware_status in ('out_of_date', 'compiling', 'updating'):
        data['webusb'] = ''
    else :
        data['webusb'] = render_to_string(
            'esphome/webusb_btn.html', {'esp_device': esp_device}
        )
    return JsonResponse(data)


@csrf_exempt
def rebuild_firmware_view(request, id):
    if request.method != 'POST':
        raise Http404()
    if not request.user.is_authenticated:
        raise Http404()
    esp_device = get_object_or_404(ESPDevice, id=id)
    rebuild_firmware.delay(esp_device.id)
    return HttpResponse('OK')


@csrf_exempt
def wifi_update_view(request, id):
    if request.method != 'POST':
        raise Http404()
    if not request.user.is_authenticated:
        raise Http404()
    esp_device = get_object_or_404(ESPDevice, id=id)
    wifi_update.delay(esp_device.id)
    return HttpResponse('OK')
