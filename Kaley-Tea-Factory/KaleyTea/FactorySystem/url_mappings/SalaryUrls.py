from django.contrib import admin
from django.urls import path, include

from FactorySystem.view_mappings import SalaryViews

urlpatterns = [
    path('FullDetails/', SalaryViews.full_details),
    path('FullDetails/FullDetails/', SalaryViews.full_details),
    path('FullDetails/final_salary_view_search', SalaryViews.final_salary_view_search),
    path('FullDetails/FullDetails', SalaryViews.full_details),
    path('FullDetails/SearchEmployee', SalaryViews.salary_employee),
    path('FullDetails/FullDetails/SearchEmployee', SalaryViews.salary_employee),
    path('FullDetails/employee_salary', SalaryViews.employee_salary, name='employee_salary'),
    path('employee_salary', SalaryViews.employee_salary, name='employee_salary'),
    path('FullDetails/SearchEmployee/employee_salary', SalaryViews.employee_salary, name='employee_salary'),
    path('delete_salary<int:id>', SalaryViews.delete_salary, name='delete_salary'),
    path('CalculateSalary/', SalaryViews.calculate_salary),
    path('Allowance/', SalaryViews.allowance),
    path('Funds/', SalaryViews.display_funds),
    path('change_rates<int:id>', SalaryViews.change_rates, name='change_rates'),
    path('update_funds<int:id>', SalaryViews.update_funds, name='update_funds'),
    path('AddAllowance/', SalaryViews.add_allowance),
    path('AddAllowance/add_allowance', SalaryViews.add_allowance),
    path('edit_allowance<int:id>', SalaryViews.edit_allowance, name='edit_allowance'),
    path('update_allowance<int:id>', SalaryViews.update_allowance, name='update_allowance'),
    path('delete_allowance<int:id>', SalaryViews.delete_allowance, name='delete_allowance'),
    path('monthly_salary/<str:year>/<str:month>', SalaryViews.monthly_salary, name='monthly_salary'),
    path('employee_salary_report<int:id>', SalaryViews.employee_salary_report, name='employee_salary_report')
]