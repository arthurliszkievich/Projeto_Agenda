from django.contrib import admin
from contact.models import Contact
from contact.models import Category

# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "created_date")
    ordering = ("id",)
    list_filter = ("created_date",)
    search_fields = ("id", "first_name", "last_name", "email", "phone")
    list_per_page = 10
    list_max_show_all = 50
    list_editable = ("phone",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("id",)
   