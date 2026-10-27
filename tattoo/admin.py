from django.contrib import admin

from tattoo.models import Service
from tattoo.models import Appointment
from tattoo.models import Review
from tattoo.models import Portfolio
from tattoo.models import Profile

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'duration']
    list_display_links = ('name', )

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'master']
    list_display_links = ('service', )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'rating', 'comment']
    list_display_links = ('comment', )

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'date','time', 'service', 'master', 'client', 'comment']
    list_display_links = ('service', )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'role']
    list_display_links = ('user', )