from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("email",)
    search_fields = ("email",)
