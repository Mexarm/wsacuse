from django.contrib import admin
from .models import DocImage
from django.utils.html import format_html


@admin.register(DocImage)
class DocImageAdmin(admin.ModelAdmin):
    list_display = ('img_link', 'state', 'uploaded_key', 'creation_date',
                    'source_ip_address', 'barcode_data', 'barcode_type')
    list_display_links = ('img_link',)
    search_fields = ['barcode_data']

    def img_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">descarga acuse</a>',
            obj.download_url)
