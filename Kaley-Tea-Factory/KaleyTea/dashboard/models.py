from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import *
from datetime import datetime

# Create your models here.

CATEGORY_1 = (
    ('Dry Tea Leaves', 'Dry Tea Leaves'),
    ('Light Tea Leaves', 'Light Tea Leaves'),
)
CATEGORY_2 = (
    ('Tea Powder Packets', 'Tea Powder Packets'),
    ('Tea Leaves Jars', 'Tea Leaves Jars'),
    ('Tea Bags', 'Tea Bags'),
)


# Create Class Inventory Product

class Product(models.Model):
    objects = None
    name = models.CharField(max_length=20, null=True)
    leaves_category = models.CharField(max_length=20, choices=CATEGORY_1, null=True)
    in_date = models.DateField(null=True)
    in_time = models.TimeField(null=True)
    tray_id = models.CharField(max_length=10000, null=True)
    temparature = models.FloatField(null=True)
    tea_weight = models.PositiveIntegerField(null=True)
    out_date = models.DateField(null=True)

    def __get__(self, instance, owner):
        return 5 * (instance.fahrenheit - 32) / 9

    def __set__(self, instance, value):
        instance.fahrenheit = 32 + 9 * value / 5

    class Meta:
        verbose_name_plural = 'Inventory Product'

    def __str__(self):
        return f'{self.name}-{self.tea_weight}'


# Create Class Inventory Order

class Order(models.Model):
    objects = None

    leaves_category = models.CharField(max_length=20, choices=CATEGORY_2, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(null=True)

    class Meta:
        verbose_name_plural = 'Inventory Order'

    def __str__(self):
        return f'{self.leaves_category} ordered by {self.staff.username}'

# ----------------------------------------------------------------------------------------------------------------------
# Leaf Inventory Management System Daily Production


class TeaGrades(models.Model):
    objects = None
    teaGrade = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'tea_grade'

    def __str__(self):
        return self.teaGrade


class Final_product_sub(models.Model):
    objects = None
    subID = models.IntegerField(blank=True)
    teaGrade = models.ForeignKey(TeaGrades, on_delete=models.CASCADE)
    gradeWeight = models.FloatField(validators=[MinValueValidator(0)])

    class Meta:
        db_table = "Final_product_sub"


class Final_product_Main(models.Model):
    objects = None
    subID = models.IntegerField(blank=True)
    totalWeight = models.FloatField(blank=True, validators=[MinValueValidator(0)])
    date = models.DateField(default=datetime.now)

    class Meta:
        db_table = "Final_product_Main"
