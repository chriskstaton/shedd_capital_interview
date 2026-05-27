from django.db import models


class CustomerObservation(models.Model):
    OCCUPATION_CHOICES = [
        ('professional', 'Professional'),
        ('student', 'Student'),
        ('unemployed', 'Unemployed'),
    ]
    ITEM_CHOICES = [
        ('coffee', 'Coffee'),
        ('tea', 'Tea'),
        ('juice', 'Juice'),
    ]

    customer_name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=20, choices=OCCUPATION_CHOICES)
    ordered_item = models.CharField(max_length=20, choices=ITEM_CHOICES)
    time_order_placed = models.IntegerField()
    time_order_received = models.IntegerField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} — {self.ordered_item} ({self.created_at:%Y-%m-%d %H:%M})"
