import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from xhtml2pdf import pisa

from ..forms import FundForm
from ..forms import AllowanceForm
from ..models import Allowance
from ..models import *
from ..utils import *
from django.views.generic import View
from django.http import HttpResponse
from django.template.loader import get_template


def full_details(request):
    emp_salary = EmployeeSalary.objects.all()

    var = {
        'emp_salary': emp_salary,
        'display': 'display:none'
    }

    return render(request, 'Salary/FullDetails.html', var)


def final_salary_view_search(request):

    if request.method == 'POST':

        searchYear = request.POST.get('searchYear')
        searchMonth = request.POST.get('searchMonth')

        try:
            empSearch = EmployeeSalary.objects.filter(year=searchYear, month=searchMonth)
            results = empSearch.count()

            if results > 0:

                var = {
                    'emp_salary': empSearch,
                    'year': searchYear,
                    'month': searchMonth,
                    'display': 'display:block'
                }

                return render(request, 'Salary/FullDetails.html', var)

            else:
                messages.error(request, 'No salaries for the entered date')
                return redirect('FullDetails/')

        except Exception as e:
            print(e)

    return redirect('Salary/FullDetails.html')


def salary_employee(request):
    emp_salary = EmployeeSalary.objects.all()
    empl = Employee.objects.all()

    var = {
        'emp_salary': emp_salary,
        'empl': empl,
        'display': 'display:none'
    }

    return render(request, "Salary/SalaryEmployee.html", var)


def employee_salary(request):
    searchNic = request.POST.get('searchNic')
    empSearch = Employee.objects.get(nic=searchNic)

    if empSearch:
        empId = empSearch.id
        #if results == 1:

        if request.method == 'POST':
                try:
                    salSearch = EmployeeSalary.objects.filter(emp_id=empId)
                    sal = salSearch.count()

                    if sal > 0:
                        var = {
                            'emp_salary': salSearch,
                            'empl': empSearch,
                            'display': 'display:block'
                        }

                        return render(request, "Salary/SalaryEmployee.html", var)

                    else:
                        messages.error(request, 'No salaries for the employee' + str(empId))
                        return render(request, "Salary/SalaryEmployee.html")

                except Exception as e:
                    print(e)

        else:
            messages.error(request, 'Employee does not exist')
            return render(request, "Salary/SalaryEmployee.html")
    else:
        messages.error(request, 'Employee does not exist')
        return redirect("FullDetails/SearchEmployee")

    #return render(request, "Salary/Funds.html")


def delete_salary(request, id):
    salary = EmployeeSalary.objects.get(pk=id)
    salary.delete()

    return render(request, 'Salary/FullDetails.html')


def calculate_salary(request):
    if request.method == 'POST':
        emp_id = request.POST.get('empID')
        month = request.POST.get('month')
        year = request.POST.get('year')

        empSearch = Employee.objects.filter(pk=emp_id)

        if len(empSearch) > 0:
            salarySearch = EmployeeSalary.objects.filter(emp_id=emp_id, year=year, month=month)

            if len(salarySearch) < 1:
                attendance = float(request.POST.get('attendance'))
                basic_salary_of_month = float(request.POST.get('basic_sal'))
                ot_hours = float(request.POST.get('ot_hours'))
                loans = float(request.POST.get('loans'))

                ot_amount = ot_hours * 100
                fund_obj = Funds.objects.first()

                etf_r = float(fund_obj.emp_etf)
                epf_empee_r = float(fund_obj.epf_employee)
                epf_emper_r = float(fund_obj.epf_employer)

                etf = basic_salary_of_month * etf_r / 100
                epf_empee = basic_salary_of_month * epf_empee_r / 100
                epf_emper = basic_salary_of_month * epf_emper_r / 100

                emp_allowance = 0
                incent1 = 0
                incent2 = 0

                allowanceSearch = Allowance.objects.filter(emp_id=emp_id)

                if len(allowanceSearch) > 0:
                    for elems in allowanceSearch.iterator():
                        emp_allowance += float(elems.allowance_by_price)
                        incent1 += float(elems.incentive_1)
                        incent2 += float(elems.incentive_2)

                total = basic_salary_of_month + ot_amount - etf - epf_emper - epf_empee + emp_allowance + incent1 + incent2

                salary = EmployeeSalary()
                salary.emp_id = Employee.objects.get(pk=emp_id)
                salary.month = month
                salary.year = year
                salary.attendance_on_month = attendance
                salary.basic_salary_of_month = basic_salary_of_month
                salary.ot_hours = ot_hours
                salary.ot_amount_for_month = ot_amount
                salary.etf = etf
                salary.epf_employee = epf_empee
                salary.epf_employer = epf_emper
                salary.loan = loans
                salary.total_salary = total
                salary.save()

                messages.success(request, 'Employee Salary added successfully')
            else:
                messages.error(request, "This employee salary already calculated")
        else:
            messages.error(request, 'Employee ID invalid')

    return render(request, 'Salary/CalculateSalary.html')


def allowance(request):
    allowance = Allowance.objects.all()
    return render(request, 'Salary/Allowance.html', {'allowance': allowance})


def add_allowance(request):
    allowance = AllowanceForm()
    if request.method == 'POST':
        allowance = AllowanceForm(request.POST)
        if allowance.is_valid():
            try:
                allowance.save()
                return render(request, 'Salary/Allowance.html')
            except:
                pass
    var = {'allowance': allowance}
    return render(request, 'Salary/AddAllowance.html', var)


def update_allowance(request, id):
    allowance_update = Allowance.objects.get(pk=id)
    allowance = AllowanceForm(request.POST, instance=allowance_update)

    if allowance.is_valid():
        allowance.save()
        messages.success(request, 'Record Updated Successfully')
        var = {'allowance_update': allowance_update}

        return render(request, 'Salary/Allowance.html', var)


def edit_allowance(request, id):
    allowance_edit = Allowance.objects.get(pk=id)

    form = AllowanceForm(instance=allowance_edit)

    var = {'allowanceForm': form, 'Aid': id}
    return render(request, 'Salary/EditAllowance.html', var)


def delete_allowance(request, id):
    allowance = Allowance.objects.get(pk=id)
    allowance.delete()

    return render(request, 'Salary/Allowance.html')


def display_funds(request):
    # check funds table
    fund_obj = Funds.objects.first()
    if fund_obj is None:
        fund = FundForm()
        fund_obj = fund.save(commit=False)
        fund_obj.emp_etf = 3
        fund_obj.epf_employee = 8
        fund_obj.epf_employer = 12

        fund_obj.save()

    funds = Funds.objects.all()
    return render(request, 'Salary/Funds.html', {'funds': funds})


def change_rates(request, id):
    fund_edit = Funds.objects.get(pk=id)

    form = FundForm(instance=fund_edit)

    var = {'fundForm': form, 'Fid': id}
    return render(request, 'Salary/ChangeRates.html', var)


def update_funds(request, id):
    funds_update = Funds.objects.get(pk=id)

    funds_2 = FundForm(request.POST, instance=funds_update)

    if funds_2.is_valid():
        funds_2.save()
        messages.success(request, 'Record Updated Successfully')
        var = {'funds_update': funds_update}

        messages.success(request, 'Product successfully added to the list.')
        return render(request, 'Salary/Funds.html')


def monthly_salary(request, year, month):
    template_path = 'Salary/MonthlyReport.html'
    print(year)
    print(month)

    empSearch = EmployeeSalary.objects.filter(year=year, month=month)
    results = empSearch.count()

    if results > 0:
        context = {
            'emp_salary': empSearch,
            'year': year,
            'month': month,
            'date': datetime.now().date()
        }

        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'filename="Monthly Salary Report.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        messages.error(request, 'No salaries for the entered date')
        return render(request, 'Salary/Funds.html')



def employee_salary_report(request, id):
    template_path = 'Salary/FullSalaryReport.html'

    empSearch = Employee.objects.get(pk=id)
    salSearch = EmployeeSalary.objects.filter(emp_id=id)

    context = {
        'emp_salary': salSearch,
        'empl': empSearch,
        'date': datetime.now().date()
    }

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="Monthly Salary Report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response