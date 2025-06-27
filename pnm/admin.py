from django.contrib import admin
from .models import Asset, Manager, AssetManager, TripDetails, DieselEntry, Breakdown, Notification

# Register Asset model
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_id', 'registration_no', 'name', 'type')
    search_fields = ('asset_id', 'registration_no', 'name', 'type')
    list_filter = ('type', 'owner')
    ordering = ('-last_updated',)

# Register Manager model
@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user__email')
    search_fields = ('name', 'user__email')

# Register AssetManager model
@admin.register(AssetManager)
class AssetManagerAdmin(admin.ModelAdmin):
    list_display = ('asset', 'manager', 'site', 'date_assigned')
    search_fields = ('asset__name', 'manager__name', 'site')
    list_filter = ('site',)
    ordering = ('-date_assigned',)

# Register TripDetails model
@admin.register(TripDetails)
class TripDetailsAdmin(admin.ModelAdmin):
    list_display = ('asset', 'date', 'from_location', 'to_location', 'distance', 'net_weight', 'deal_type')
    search_fields = ('asset__name', 'from_location', 'to_location')
    list_filter = ('deal_type',)
    ordering = ('-date',)

# Register DieselEntry model
@admin.register(DieselEntry)
class DieselEntryAdmin(admin.ModelAdmin):
    list_display = ('asset', 'date', 'quantity', 'rate', 'reading', 'site')
    search_fields = ('asset__name', 'site')
    list_filter = ('site',)
    ordering = ('-date',)

# Register Breakdown model
@admin.register(Breakdown)
class BreakdownAdmin(admin.ModelAdmin):
    list_display = ('asset', 'date', 'site', 'status', 'mechanic', 'estimated_delivery_date', 'delivered_at_date')
    search_fields = ('asset__name', 'site', 'mechanic')
    list_filter = ('status',)
    ordering = ('-date',)

# Register Notification model
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'created_at', 'is_read')
    search_fields = ('recipient__username', 'notification_type')
    list_filter = ('notification_type', 'is_read')
    ordering = ('-created_at',)
