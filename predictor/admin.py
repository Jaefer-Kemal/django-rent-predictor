from django.contrib import admin

from predictor.models import HousingData

@admin.register(HousingData)
class HousingAdmin(admin.ModelAdmin):
    list_display = ("csv_file",)