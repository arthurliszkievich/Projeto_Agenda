from django.contrib import admin
from contact.models import Contact
from contact.models import Category

# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "created_date",
        "show",
    )
    ordering = ("id",)
    search_fields = ("id", "first_name", "last_name", "email", "phone")
    list_per_page = 10
    list_max_show_all = 50
    list_editable = ("first_name", "last_name", "phone", "show")
    list_display_links = ("id",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("id",)
