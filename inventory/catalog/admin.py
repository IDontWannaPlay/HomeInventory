from django.contrib import admin
from catalog.models import Category, Item, ItemInstance

# Register your models here.
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemInstance)
