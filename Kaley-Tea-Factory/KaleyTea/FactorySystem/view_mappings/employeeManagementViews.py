from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import *
from django.http import HttpResponse
from django.views.generic.base import View
from ..common_utils.employeeManagement_pdf import render_to_pdf


# Create your views here.




def attendance_management(request):

    if request.method == 'POST':

        dateView = request.POST.get('date')

        attend = attendance.objects.filter(date=dateView).select_related('empID')

        return render(request, 'EmployeeManagement_templates/attendance_management.html', {'attendance': attend, 'date': dateView})

    return redirect('attendance_date')



def updatemark_attendance(request):

    if request.method == 'POST':

       date = request.POST.get('date')
       empId = request.POST.get('workersid')
       type = request.POST.get('dayType')

       attend = attendance.objects.get(empID=empId, date=date)

       try:

            if type is not None:

                if type == 'halfDay':
                    type = 'HalfDay'

                else:
                    type = 'FullDay'

                print(type)

                #present
                attend.attendaceStatus = "Present"
                attend.daytype = type
                attend.save()

            else:
                 # absent
                 attend.attendaceStatus = "Absent"
                 attend.daytype = None
                 attend.save()


            attend = attendance.objects.filter(date=date).select_related('empID')

            return render(request, 'EmployeeManagement_templates/attendance_management.html', {'attendance': attend, 'date': date})


       except Exception as e:
        print(e)

    return redirect('attendance_date')




def staff_management(request):

    arr = Employee.objects.filter(empGroup='staff')

    return render(request, 'EmployeeManagement_templates/staff_management.html', {'Employee': arr})



def factoryworkers_management(request):

    arr = Employee.objects.filter(empGroup='factory_Worker')

    return render(request, 'EmployeeManagement_templates/factoryworkers_management.html', {'Employee': arr})



def showAttendance(request):
    arr = Employee.objects.filter(empGroup='factory_Worker')
    workingDays = attendance.workingDays

    return render(request, 'EmployeeManagement_templates/attendance_management.html', {'Employee': arr}, workingDays)



def selectAttendence(request):

    return render(request, 'EmployeeManagement_templates/attendance_date.html')



def viewMarkAttendance(request):

    if request.method == 'POST':

        date = request.POST.get('currDate')

        attend = attendance.objects.filter(date=date).filter(attendaceStatus__in=['Present', 'Absent']).values('empID')
        arr = Employee.objects.exclude(id__in=attend).all()

        return render(request, 'EmployeeManagement_templates/mark_attendance.html', {'Employee': arr, 'date': date})

    return redirect('attendance_date')




def markAttendance(request):

    if request.method == 'POST':
        empID = request.POST.get('workersid')
        dayType = request.POST.get('dayType')
        date = request.POST.get('date')
        emp = Employee.objects.get(pk=empID)
        try:

            if dayType is not None:

                dayt = 'FullDay'

                if dayType == 'halfDay':
                    dayt = 'HalfDay'

                #present
                attend = attendance()
                attend.date = date
                attend.empID = emp
                attend.attendaceStatus = "Present"
                attend.daytype = dayt
                attend.save()

            else:
                 # absent
                 attend = attendance()
                 attend.date = date
                 attend.empID = emp
                 attend.attendaceStatus = "Absent"
                 attend.save()

            atten = attendance.objects.filter(date=date).filter(attendaceStatus__in=['Present', 'Absent'])\
                .values('empID')
            arrEmp = Employee.objects.exclude(id__in=atten).filter(empGroup='factory_Worker')
            messages.success(request, 'Successfully Added Details')
            return render(request, 'EmployeeManagement_templates/mark_attendance.html', {'Employee': arrEmp, 'date': date})

        except Exception as e:
            print(e)

    return redirect('attendance_date')



def edit_employee(request):

    if request.method == "POST":
        eid = request.POST.get('workersid')

        if eid is not None:

            try:
                employee = Employee.objects.get(pk=eid)
                eform = RegisterEmployee(instance=employee)
                return render(request, 'EmployeeManagement_templates/edit_employee.html', {'form': eform , 'EmpId' : eid})

            except Exception as e:
                print(e)

        else:
            pass

    return render(request, 'EmployeeManagement_templates/edit_employee.html')



def update_employee(request):

    if request.method == 'POST':
        eid = request.POST.get('empId')

        if eid is not None:
            employee = Employee.objects.get(pk=eid)
            form = RegisterEmployee(request.POST, instance=employee)

            if form.is_valid():
                form.save()
                try:

                    if (form.cleaned_data.get('empGroup') == 'factory_Worker'):
                        messages.success(request, 'update successful')
                        return redirect('factoryworkers_management')

                    else:
                        messages.success(request, 'update successful')
                        return redirect('staff_management')

                except Exception as e:
                    print(e)
                    messages.success(request, 'Exception:' + e)

            else:
                messages.error(request, "Can't Update Details.")
                return redirect('edit_employee')

        else:
            messages.error(request, "Can't Update Details.")
            return redirect('edit_employee')



def view_employee(request):

    id = request.POST.get("workersid")

    employee = Employee.objects.get(pk=id)

    return render(request, 'EmployeeManagement_templates/view_employee.html', {'employee':employee})



def employee_registration(request):
    form = RegisterEmployee()

    if request.method == 'POST':
        form = RegisterEmployee(request.POST)
        print(form.errors)
        if form.is_valid():
            try:
                form.save()
                if (form.cleaned_data.get('empGroup') == 'factory_Worker'):
                    messages.success(request, 'Factory worker added successfully')
                    return redirect('factoryworkers_management')
                else:
                    messages.success(request, 'Staff added successfully')
                    return redirect('staff_management')

            except Exception as e:
                print(e)
                messages.success(request, 'Exception:' +e)

        else:
            print(form.errors)
            messages.error(request, 'Invalid Details')
            pass

    var = {'form': form}
    return render(request, 'EmployeeManagement_templates/employee_registration.html', var)



def deleteEmployee(request):
    workersid = request.POST.get('workersid')
    print(workersid)

    if request.method == 'POST' and workersid is not None:
        worker = Employee.objects.get(id=workersid)

        workerType = worker.empGroup

        worker.delete()

        if workerType == 'staff':
            messages.success(request, 'Employee Deleted successfully')
            return redirect('staff_management')

        else:
            messages.success(request, 'Employee Deleted successfully')
            return redirect('factoryworkers_management')


class GeneratePDFMonthlyAttendance(View):
    def get(self, request, *args, **kwargs):

        dateView = request.GET.get('date')

        attend = attendance.objects.filter(date=dateView).select_related('empID')

        context = {
            'attendance': attend,
            'date': dateView
        }

        pdf = render_to_pdf('EmployeeManagement_templates/monthlyAttendancePDF.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            return response

        else:
            return redirect('attendance_date')
