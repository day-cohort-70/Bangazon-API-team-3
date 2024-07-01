from django.db import models


class OrderProduct(models.Model):

    order = models.ForeignKey("Order",
                              on_delete=models.DO_NOTHING,
                              related_name="line_items")

    product = models.ForeignKey("Product",
                                on_delete=models.DO_NOTHING,
                                related_name="line_items")
    
    cart_quantity = models.IntegerField(default=1)
