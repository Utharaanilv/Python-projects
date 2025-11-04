from django.contrib import admin
from django.utils.html import format_html
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'comment', 'image_thumbnail', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'comment')

    # ✅ Disable Add button
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False  #  Disable Edit

    # 🖼 Show thumbnail in list view
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 6px; border:1px solid #ccc;" />',
                obj.image.url
            )
        return 'No Image'
    image_thumbnail.short_description = 'Image'

    # 🖼 Larger preview in detail view
    readonly_fields = ('image_preview',)  # This adds preview but not editable

    fieldsets = (
        (None, {
            'fields': ('user', 'booking', 'rating', 'comment', 'image', 'image_preview', 'created_at')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<div style="border: 1px solid #ddd; border-radius: 10px; padding: 10px; display: inline-block;">'
                '<img src="{}" style="max-width: 400px; max-height: 400px; object-fit: cover; border-radius: 8px;" />'
                '</div>',
                obj.image.url
            )
        return 'No image uploaded'
    image_preview.short_description = 'Image Preview'