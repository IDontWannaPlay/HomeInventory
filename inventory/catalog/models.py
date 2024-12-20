from django.db import models

# Create your models here.
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

class Category(models.Model):
    """Model representing item category."""

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a category for an item (e.g. Food, Utensil, Tool etc.)"
    )


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item-detail', args=[str(self.id)])

class Location(models.Model):
    name = models.CharField(max_length=200)
    parent_location = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_locations')

    def get_full_path(self):
        if self.parent_location:
            return f"{self.parent_location.get_full_path()} -> {self.name}"
        return self.name
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('location-detail', args=[str(self.id)])

class ItemLocation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['item', 'location'], name='unique_item_location')
        ]

    def __str__(self):
        return f"{self.item.name} in {self.location.name}"
    
    def get_full_path(self):
        return f"{self.item.name} is located at {self.location.get_full_path()}"