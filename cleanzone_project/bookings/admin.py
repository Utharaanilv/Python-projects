from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service_label', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__username',)

    #  Disable Add button
    def has_add_permission(self, request):
        return False

    # Remove assigned_employee from list_editable for now (must be a real field)
    list_editable = ('status',)

    def service_label(self, obj):
        """Display the service name or type properly."""
        if hasattr(obj, 'service') and obj.service:
            return obj.service.name
        if hasattr(obj, 'get_service_type_display'):
            return obj.get_service_type_display()
        return getattr(obj, 'service_type', '-')
    service_label.short_description = 'Service'
