from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import mark_safe
from .models import ESPDevice
from .forms import ESPDeviceAdminForm


@admin.register(ESPDevice)
class ESPDeviceAdmin(admin.ModelAdmin):
    form = ESPDeviceAdminForm
    search_fields = 'name',
    list_display = 'name', 'board', 'firmware_status', 'connection_display'
    list_filter = 'firmware_status', 'connected'
    readonly_fields = (
        'api_secret_display', 'install_button',
        'current_config_display', 'firmware_status',
        'occupied_pins', 'components_display', 'connected'
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return [
                (None, {'fields': [
                    'name', 'platform', 'board', 'wifi_ssid', 'wifi_password',
                ]})
            ]
        fieldsets = [
            (None, {'fields': [
                'id','name', 'platform', 'board', 'wifi_ssid', 'wifi_password',
                'api_secret_display',
            ]}),
            ("Components", {'fields': [
                'components_display', 'occupied_pins'
            ]}),
            ("Status/Firmware", {'fields': [
                'connected', 'firmware_status', 'log', 'install_button'
            ]}),
            ("Advanced", {
                'fields': ['dallas_hub', 'additional_yaml', 'current_config_display'],
                'classes': ('collapse',),
            })
        ]
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('name', 'platform', 'board')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.firmware_status = 'out_of_date'
            return obj.save()

        org = None
        if obj.id:
            org = ESPDevice.objects.get(id=obj.id)
        if org and (
            org.wifi_ssid != obj.wifi_ssid
            or org.wifi_password != obj.wifi_password
        ):
            obj.firmware_status = 'out_of_date'

        return obj.save()

    def current_config_display(self, obj=None):
        if not obj:
            return ''
        return mark_safe(
            obj.get_current_config().replace(' ', '&nbsp;').replace('\n', '<br>')
        )
    current_config_display.short_description = 'final config'

    def api_secret_display(self, obj=None):
        if not obj:
            return ''
        help_text = ''
        for field in obj._meta.fields:
            if field.name == 'api_secret':
                help_text = field.help_text
                break
        return mark_safe(render_to_string(
                'admin/show_secret.html', {
                    'secret': obj.api_secret,
                    'help_text': help_text,
                    'object_id': obj.id
                }
            ))
    api_secret_display.short_description = 'API secret'

    def install_button(self, obj):
        # updated via ajax.
        return ''
    install_button.short_description = 'USB'

    def components_display(self, obj):
        if obj.pk:
            return mark_safe(', '.join([
                '<a href="%s">%s</a>' % (comp.get_admin_url(), str(comp))
                for comp in obj.components.all()
            ]))
    components_display.short_description = 'Components'

    def connection_display(self, obj):
        if not obj:
            return ''
        return render_to_string(
            'admin/esp_connection_display.html', {'obj': obj}
        )
    connection_display.short_description = "WiFi connection"
