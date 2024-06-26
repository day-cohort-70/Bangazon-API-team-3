from django.db import models
from .customer import Customer


class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
