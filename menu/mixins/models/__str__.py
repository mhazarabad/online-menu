from django.db import models

class NameStrMixin(models.Model):
    class Meta:
        abstract = True
    
    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        return super().__str__()

class CompositeStrMixin(models.Model):
    class Meta:
        abstract = True
    
    def __str__(self):
        parts = []
        if hasattr(self, 'food') and hasattr(self, 'topping'):
            parts.append(f"{self.food.name} - {self.topping.name}")
        elif hasattr(self, 'food'):
            parts.append(f"{self.food.name} - Image")
        else:
            parts.append(super().__str__())
        return "".join(parts)
