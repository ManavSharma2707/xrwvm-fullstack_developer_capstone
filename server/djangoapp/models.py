from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class CarMake(models.Model):
    """A car manufacturer, e.g. Toyota."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    founded_year = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1800), MaxValueValidator(2100)])
    website = models.URLField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """A model sold by a manufacturer (many models belong to one make)."""
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]

    car_make = models.ForeignKey(
        CarMake, on_delete=models.CASCADE, related_name='models')
    # Id of the dealership (stored in MongoDB) that sells this model
    dealer_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CAR_TYPES, default=SEDAN)
    year = models.IntegerField(
        default=2023,
        validators=[MaxValueValidator(2023), MinValueValidator(2015)])
    color = models.CharField(max_length=50, blank=True)
    mileage = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=now, editable=False)

    class Meta:
        ordering = ['car_make__name', 'name']

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
