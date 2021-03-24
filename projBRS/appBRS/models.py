from django.db import models
from django.contrib.auth.models import User


class userInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=12)
    proof_of_user = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Bike(models.Model):
    BIKE_COLOR_CHOICES = [
        ("Red", "Red"),
        ("White", "White"),
        ("Black", "Black"),
        ("Blue", "Blue"),
    ]

    BIKE_TYPE_CHOICES = [
        ("Regular", "Regular"),
        ("Non Gear", "Non Gear"),
        ("Sports", "Sports"),
    ]

    bike_number = models.CharField(primary_key=True, max_length=10)
    bike_color = models.CharField(max_length=20, choices=BIKE_COLOR_CHOICES)
    bike_quantity = models.PositiveIntegerField()
    bike_type = models.CharField(max_length=20, choices=BIKE_TYPE_CHOICES)
    bike_model = models.CharField(max_length=30)
    bike_view = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.bike_number


class Rent(models.Model):
    hourly_rent = models.PositiveIntegerField()
    daily_rent = models.PositiveIntegerField()
    weekly_rent = models.PositiveIntegerField()
    hourly_penalty = models.PositiveIntegerField()
    daily_penalty = models.PositiveIntegerField()
    weekly_penalty = models.PositiveIntegerField()
    bike_rent = models.ForeignKey(Bike, on_delete=models.CASCADE)
