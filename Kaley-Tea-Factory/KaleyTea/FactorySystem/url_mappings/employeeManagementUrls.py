from django.urls import path
from FactorySystem.view_mappings import employeeManagementViews
from FactorySystem.view_mappings.employeeManagementViews import *

urlpatterns = [

    path('selectAttendence', employeeManagementViews.selectAttendence, name="attendance_date"),
    path('viewMarkAttendance', employeeManagementViews.viewMarkAttendance, name="viewMarkAttendance"),
    path('markAttendance', employeeManagementViews.markAttendance, name="mark_attendance"),
    path('attendance_management', employeeManagementViews.attendance_management, name="attendance_management"),
    path('updatemark_attendance', employeeManagementViews.updatemark_attendance, name="updatemark_attendance"),

    path('staff_management', employeeManagementViews.staff_management, name="staff_management"),
    path('factoryworkers_management', employeeManagementViews.factoryworkers_management, name="factoryworkers_management"),
    path('factoryworkers_management/delete', employeeManagementViews.deleteEmployee, name="delete_employee"),
    path('edit_employee', employeeManagementViews.edit_employee, name="edit_employee"),
    path('update_employee', employeeManagementViews.update_employee, name="update_employee"),
    path('view_employee', employeeManagementViews.view_employee, name="view_employee"),
    path('staff_management/AddEmployee', employeeManagementViews.employee_registration, name="employee_registration1"),
    path('factoryworkers_management/AddEmployee', employeeManagementViews.employee_registration,name="employee_registration2"),
    path('factoryworkers_management/printDailyReport', GeneratePDFMonthlyAttendance.as_view(), name="printDailyReport"),

]

