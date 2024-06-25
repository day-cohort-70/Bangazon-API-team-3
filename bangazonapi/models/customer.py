from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
    )
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=55)
    liked_products = models.ManyToManyField(
        "Product", through="Like", related_name="liked_by"
    )

    @property
    def recommends(self):
        return self.__recommends

    @recommends.setter
    def recommends(self, value):
        self.__recommends = value
