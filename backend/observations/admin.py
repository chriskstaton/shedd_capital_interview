from django.contrib import admin
from .models import CustomerObservation


@admin.register(CustomerObservation)
class CustomerObservationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'occupation', 'ordered_item', 'time_order_placed', 'time_order_received', 'rating', 'created_at']
    list_filter = ['occupation', 'ordered_item', 'rating']
    search_fields = ['customer_name']
    readonly_fields = ['created_at']
