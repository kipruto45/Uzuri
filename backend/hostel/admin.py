from django.contrib import admin

from .models import Hostel, Room, HostelApplication, RoomAllocation
from django.contrib import admin

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
	list_display = ('name', 'location')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
	list_display = ('hostel', 'number', 'capacity', 'current_occupants', 'is_active')
	list_filter = ('hostel', 'is_active')

@admin.register(HostelApplication)
class HostelApplicationAdmin(admin.ModelAdmin):
	list_display = ('student', 'room', 'semester', 'status', 'decline_reason', 'created_at')
	list_filter = ('status', 'semester')
	search_fields = ('student__user__username', 'room__number')

@admin.register(RoomAllocation)
class RoomAllocationAdmin(admin.ModelAdmin):
	list_display = ('student', 'room', 'semester', 'allocated_at')
	list_filter = ('semester',)
