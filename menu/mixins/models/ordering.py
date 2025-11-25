from django.db import models

class OrderingMixin(models.Model):
    is_available = models.BooleanField(default=True, help_text='If the food is available for ordering')
    discount = models.FloatField(default=0, blank=True, null=True, help_text='The discount percentage for the food')
    available_from = models.TimeField(blank=True, null=True, help_text='The time from which the food is available for ordering')
    available_to = models.TimeField(blank=True, null=True, help_text='The time until which the food is available for ordering')

    class Meta:
        abstract = True

