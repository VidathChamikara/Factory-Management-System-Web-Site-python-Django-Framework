from django import forms
from .models import Product, Order, TeaGrades, Final_product_sub, Final_product_Main


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'leaves_category', 'in_date', 'in_time', 'tray_id', 'temparature', 'tea_weight', 'out_date']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['staff', 'leaves_category', 'order_quantity', 'time']


# ---------------------------------------------------------------------------------------------------------------------
# Inventory Daily Production Management System

class AddSubProductForm(forms.ModelForm):
    class Meta:
        model = Final_product_sub
        fields = '__all__'


class AddMainProductForm(forms.ModelForm):
    class Meta:
        model = Final_product_Main
        fields = '__all__'


class AddTeaGradeform(forms.ModelForm):
    class Meta:
        model = TeaGrades
        fields = '__all__'
