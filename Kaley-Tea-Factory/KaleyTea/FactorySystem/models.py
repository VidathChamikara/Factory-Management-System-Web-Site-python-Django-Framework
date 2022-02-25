from django.db import models
from datetime import *
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator


# -----Employee Management
from FactorySystem.common_utils.validators import nic_validator


class Employee(models.Model):
    GENDER=(
        ('Male','Male'),
        ('Female','Female'),
    )
    MARITALSTATUS=(
        ('Married','Married'),
        ('UnMarried','Unmarried'),
    )
    EMPLOYEETYPE=(
        ('Permanent','Permanent'),
        ('Temparory','Temparory'),
    )
    EMPGROUP = (
        ('staff', 'Staff'),
        ('factory_Worker', 'FactoryWorker'),
    )
    DESIGNATION = (
        ('Factory_Officer', 'Factory_Officer'),
        ('AssistantFactory_Officer', 'AssistantFactory_Officer'),
        ('Clerk', 'Clerk'),
        ('Trainee', 'Trainee'),
        ('Supervisor', 'Supervisor'),
        ('Cashier', 'Cashier'),
        ('Driver','Driver'),
    )

    nic = models.CharField(max_length=12, unique=True, validators=[nic_validator])
    epfNo = models.IntegerField(unique=True, null=True, validators=[
        RegexValidator(
            regex='^[0-9]*$',
            message='EPF No can only contain positive numbers',
            code='EPF No is invalid'
        )
    ])
    name = models.CharField(max_length=50)
    address = models.TextField(null=True)
    gender = models.CharField(max_length=50, choices=GENDER)
    dob = models.DateField(null=True)
    maritalStatus = models.CharField(max_length=50, choices=MARITALSTATUS)
    contactNo = models.CharField(max_length=10, null=True, validators=[
        RegexValidator(
            regex='^[0-9]*$',
            message='Contact No can only contain numbers',
            code='Invalid Contact No '
        ),
        RegexValidator(
            regex='^.{10}$',
            message='Contact No length is invalid',
            code='Invalid Contact No ',
        )
    ])
    doa = models.DateField(null=True)
    basicSalary = models.FloatField(null=True)
    empType = models.CharField(max_length=50, choices=EMPLOYEETYPE,null=True)
    empGroup = models.CharField(max_length=50, choices=EMPGROUP, null=True)
    designation = models.CharField(max_length=50, choices=DESIGNATION,null=True, blank=True)


class attendance(models.Model):
    DAYTYPE = (
        ('FD', 'FullDay'),
        ('HD', 'HalfDay'),
    )
    STATUS = (
        ('Pres', 'Present'),
        ('Abs', 'Absent'),
    )
    date = models.DateField(blank=True)
    daytype = models.CharField(max_length=20, choices=DAYTYPE, blank=True)
    attendaceStatus = models.CharField(max_length=50, choices=STATUS, blank=True)
    empID = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="attendance", null=True
    )

    class Meta:
        unique_together = (('date', 'empID'),)


# ------ Salary-Nadeesh
class Funds(models.Model):
    emp_etf = models.FloatField()
    epf_employee = models.FloatField()
    epf_employer = models.FloatField()

    class Meta:
        db_table = "funds"


class EmployeeSalary(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance_on_month = models.FloatField()
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=20)

    basic_salary_of_month = models.FloatField()

    etf = models.FloatField(null=True)
    epf_employee = models.FloatField(null=True)
    epf_employer = models.FloatField(null=True)

    ot_hours = models.IntegerField(null=True)
    ot_amount_for_month = models.FloatField(null=True)

    loan = models.FloatField(null=True)

    total_salary = models.FloatField(null=True)

    class Meta:
        db_table = 'Employee_salary'


class Allowance(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    allowance_by_price = models.FloatField()
    incentive_1 = models.FloatField()
    incentive_2 = models.FloatField()

    class Meta:
        db_table = "allowance"


# -----------------------------------------------------------------------------------------------------------
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_category = models.CharField(max_length=50)
    product_weight = models.FloatField()

    class Mete:
        db_table = 'Product'

        
# Tea shop inventory
class CategoryProduct(models.Model):
    cp_name = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)

    class Meta:
        unique_together = (('category', 'weight'),)

    def __str__(self):
        return self.cp_name


class AddPackets(models.Model):

    date = models.DateField()
    noOfPackets = models.IntegerField(validators=[MinValueValidator(1)])
    categoryProductID = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE)


class Stock(models.Model):
    category = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    available_stock = models.IntegerField()

    class Meta:
        unique_together = (('category', 'weight'),)


# -------------------------------------------- Tea shop Sales ---------------------------------------
class ProductPrice(models.Model):
    product = models.OneToOneField(CategoryProduct, on_delete=models.CASCADE, primary_key=True)
    product_price = models.FloatField(validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'ProductPrice'

       
class Bill(models.Model):
    Date = models.DateField(blank=True)
    Time = models.TimeField(blank=True)
    Total_amount = models.FloatField(validators=[MinValueValidator(0)])
    Given_cash_amount = models.FloatField(validators=[MinValueValidator(0)])
    Handled_by = models.CharField(max_length=50)

    class Meta:
        db_table = 'Bill'


class BillProduct(models.Model):
    Bill_Number = models.ForeignKey(Bill, on_delete=models.CASCADE)
    Product = models.IntegerField()
    Price = models.FloatField(validators=[MinValueValidator(0)])
    QTY = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'Bill_Product'
        unique_together = (("Bill_Number", "Product"), )


# if a product is deleted it will move to this table. then BillProducts can get the details from this
class DeletedProduct(models.Model):
    id = models.IntegerField(primary_key=True)
    cp_name = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)

    class Meta:
        unique_together = (('category', 'weight'),)

    def __str__(self):
        return self.cp_name


class Cart(models.Model):
    product = models.OneToOneField(ProductPrice, on_delete=models.CASCADE, primary_key=True)
    QTY = models.IntegerField(validators=[MinValueValidator(0)], default=1, blank=True)

    class Meta:
        db_table = 'Cart'

        
# --------------------------- Stock sales and auction stock ---------------
class Newuser(models.Model):
    Username = models.CharField(max_length=150)
    Email = models.CharField(max_length=150)

    class Meta:
        db_table = 'Newuser'


class buyers(models.Model):
    Cname = models.CharField(max_length=150)
    regNo = models.CharField(max_length=150)
    Address = models.CharField(max_length=150)
    PNumber = models.CharField(max_length=150)

    class Meta:
        db_table = 'buyers'


class auction(models.Model):
    stockID = models.CharField(max_length=150)
    teacat = models.CharField(max_length=150)
    totWeight = models.CharField(max_length=150)
    packages = models.CharField(max_length=150)
    datePrepared = models.CharField(max_length=150)

    class Meta:
        db_table = 'auction'


class soldStock(models.Model):
    stockID = models.CharField(max_length=150)
    teacat = models.CharField(max_length=150)
    totWeight = models.CharField(max_length=150)
    packages = models.CharField(max_length=150)
    datePrepared = models.CharField(max_length=150)
    Cname = models.CharField(max_length=150)
    regNo = models.CharField(max_length=150)

    class Meta:
        db_table = 'soldStock'


class notsoldStock(models.Model):
    stockID = models.CharField(max_length=150)
    teacat = models.CharField(max_length=150)
    totWeight = models.CharField(max_length=150)
    packages = models.CharField(max_length=150)
    datePrepared = models.CharField(max_length=150)

    class Meta:
        db_table = 'notsoldStock'


# ---------- Supplier -----
# class Newuser(models.Model):
#     Username = models.CharField(max_length=150)
#     Emaill = models.CharField(max_length=150)
#
#     class Meta:
#         db_table = 'Newuser'


class Supreddeta(models.Model):
     Fullname = models.CharField(max_length=150)
     Nicno = models.CharField(max_length=150)
     Address = models.CharField(max_length=150)
     Dob = models.CharField(max_length=150)
     Email = models.CharField(max_length=150)
     Contactnum = models.CharField(max_length=150)
     Paymenttype = models.CharField(max_length=150)
     Bank= models.CharField(max_length=150)
     Accountnum = models.CharField(max_length=150)

     class Meta:
         db_table = 'Supreddeta'


class Leafstock(models.Model):
    Suppliernicc = models.CharField(max_length=150)
    Totalweight = models.CharField(max_length=150)
    Receiveddate = models.CharField(max_length=150)
    Receivedtime = models.CharField(max_length=150)

    class Meta:
        db_table = 'Leafstock'


class Paymentdata(models.Model):
    Suppliernic = models.CharField(max_length=150)
    Supplierid = models.CharField(max_length=150)
    Totalkilo = models.CharField(max_length=150)
    Totalpayment = models.CharField(max_length=150)
    Date = models.CharField(max_length=150)
    Time = models.CharField(max_length=150)

    class Meta:
        db_table = 'Paymentdata'


# transport-------------------------------------------------------------------------
class Driver(models.Model):
    licence_no = models.CharField(max_length=10)
    epfNo = models.IntegerField(null=True)

    def __str__(self):
        return self.licence_no


class Vehicle(models.Model):
    VehicleNo = models.CharField(max_length=20, unique=True)
    Driverid = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.VehicleNo


class Driving_Records(models.Model):
    Date = models.DateField(default=datetime.now)
    Start_Reading = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex='^[0-9]*$',
            message='Start reading must contain only numbers',
            code='Start date is invalid'
        )
    ])

    End_Reading = models.CharField(max_length=20,validators=[
        RegexValidator(
            regex='^[0-9]*$',
            message='End reading must contain only numbers',
            code='End date is invalid'
        )
    ])
    Meter_Difference = models.IntegerField(blank=True)
    VehicleNo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)


class Services(models.Model):
    Bill_No = models.CharField(max_length=10)
    Description = models.TextField()
    Service_Date = models.DateField(default=datetime.now)
    VehicleNo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    Amount = models.FloatField()
