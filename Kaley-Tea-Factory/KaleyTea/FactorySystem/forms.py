from django import forms
from .models import *
from .models import Newuser


# -------------------------------------------- Tea shop Sales ---------------------------------------
class AddProductPriceForm(forms.ModelForm):
    class Meta:
        model = ProductPrice
        fields = '__all__'

        
class AddItemToCart(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'


class AddBill(forms.ModelForm):
    class Meta:
        model = Bill
        fields = '__all__'


class AddBillProduct(forms.ModelForm):
    class Meta:
        model = BillProduct
        fields = '__all__'

        
class DeletedProducts(forms.ModelForm):
    class Meta:
        model = DeletedProduct
        fields = '__all__'


# Tea shop inventory
class AddTeaPacketsForm(forms.ModelForm):
    class Meta:
        model = AddPackets
        fields = '__all__'


class AddcategoryProductForm(forms.ModelForm):
    class Meta:
        model = CategoryProduct
        fields = '__all__'


class updateform(forms.ModelForm):
    class Meta:
        model = Newuser
        fields = '__all__'


class updateBuyerform(forms.ModelForm):
    class Meta:
        model = buyers
        fields = '__all__'


class updateAuctionform(forms.ModelForm):
    class Meta:
        model = auction
        fields = '__all__'


# -----Employee Management
class RegisterEmployee(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class MarkAttendance(forms.ModelForm):
    class Meta:
        model = attendance
        fields = '__all__'
        
        
# ---- Salary ----------
class FundForm(forms.ModelForm):
    class Meta:
        model = Funds
        fields = '__all__'


class AllowanceForm(forms.ModelForm):
    class Meta:
        model = Allowance
        fields = '__all__'


class EmployeeSalaryForm(forms.ModelForm):
    class Meta:
        model = EmployeeSalary
        fields = '__all__'


# class updateform(forms.ModelForm):
#     class Meta:
#         model = Newuser
#         fields = '__all__'


class supupdateform(forms.ModelForm):
    class Meta:
        model = Supreddeta
        fields = '__all__'


# Transportation
class AddVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'


class AddDriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'


class VehicleRecordsForm(forms.ModelForm):
    class Meta:
        model = Driving_Records
        fields = '__all__'


class RepairForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'
