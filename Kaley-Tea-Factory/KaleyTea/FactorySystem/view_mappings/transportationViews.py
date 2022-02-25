from django.http import HttpResponse
from django.shortcuts import render, redirect
from FactorySystem.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views import View

# Create your views here.

#transport management------------------------------------------------------------------------------------------------------------

# add vehicle

def Vehicle_Records(request):

    form = AddVehicleForm()

    if request.method == 'POST':

        form = AddVehicleForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request,"Successfully added vehicle details")
                return redirect('addVehicle')
            except Exception as e:
                print(e)
                messages.success(request, 'Exception:'+ e)

        else:
            print(form.errors)
            messages.success(request, 'Invalid Details')

    #assign all vehicle objects
    array = Vehicle.objects.all()

    #assign form
    var = {'vehicleForm': form}


    alldetails = {'Vform':var , 'AllVehicle':array }

    return render(request, 'Transport_templates/AddVehicle.html', alldetails)


# delete vehicle

def deleteVehicleRecord(request):

    id = request.POST.get('id')

    if request.method == 'POST' and id != None:
        vehicle = Vehicle.objects.get(id=id)
        vehicle.delete()

    return redirect('addVehicle')



# add driver


def driver_records(request):

    form = AddDriverForm()

    if request.method == 'POST':

        form = AddDriverForm(request.POST)

        if form.is_valid():
            try:

                form.save()
                messages.success(request, 'Successfully added driver details')
                return redirect('Transport')

            except Exception as e:
                print(e)
                messages.success(request, 'Exception:'+ e)

        else:
            print(form.errors)
            messages.success(request, 'Invalid Details')


    #assign all vehicle objects
    array = Driver.objects.all()

    #assign form
    var = {'driverForm': form}


    allDdetails = {'VDform':var , 'AllDriver':array }

    return render(request, 'Transport_templates/AddDriver.html', allDdetails)


# delete driver

def deleteDriverRecord(request):

    id = request.POST.get('id')

    if request.method == 'POST' and id != None:
        driver = Driver.objects.get(id=id)
        driver.delete()

    return redirect('Transport')


# display driver

def DisplayDriverRecord(request):

    if request.method == 'POST':
        id = request.POST.get('Did')

        if id is not None:
            try:
                driver = Driver.objects.get(pk=id)
                driverForm = AddDriverForm(instance=driver)
                return render(request, 'Transport_templates/UpdateDriver.html', {'Dform': driverForm, 'DId':id})

            except Exception as e:
                print(e)

        else:
            pass

    else:
        pass

    return redirect('Transport')


# update driver records

def UpdateDriverRecord(request):

    if request.method == 'POST':
        dID = request.POST.get('DID')

        if dID is not None:

            try:
                driver = Driver.objects.get(pk=dID)
                form_update = AddDriverForm(request.POST, instance=driver)

                if form_update.is_valid():
                    form_update.save()
                    messages.success(request, 'Successfully update driver details')
                    return redirect('Transport')


            except Exception as e:
                print(e)
                messages.success(request, 'Invalid Details')


    return redirect('Transport')



# add vehicle driving records

def DrivingRecords(request):

    form = VehicleRecordsForm()
    diff = 0

    if request.method == 'POST':

        form = VehicleRecordsForm(request.POST)

        if form.is_valid():
            try:
                start = form.cleaned_data['Start_Reading']
                end = form.cleaned_data['End_Reading']
                diff = int(end) - int(start)

                if diff > 0:

                    form_mread = form.save(commit=False)
                    form_mread.Meter_Difference = diff

                    form_mread.save()
                    messages.success(request, 'Successfully added driving records')
                    return redirect('RecordTable')

                else:
                    messages.error(request, 'End reading Number Error')

            except Exception as e:
                print(e)
                messages.error(request, 'Exception:' + e)

        else:
            print(form.errors)
            messages.error(request, 'Invalid Details')

    # assign form
    var = {'RecordForm': form}

    return render(request, 'Transport_templates/VehicleRecords.html', var)


#show driving records

def ShowDrivingRecords(request):

    records = Driving_Records.objects.all()

    return render(request, 'Transport_templates/VehicleRecordsTable.html', {'records': records})



# delete vehicle driving records

def deleteRecords(request):

    id = request.POST.get('id')

    if request.method == 'POST' and id != None:
        record = Driving_Records.objects.get(id=id)
        record.delete()

    return redirect('RecordTable')


# add vehicle repairs

def AddVehicleRepairs(request):

    form = RepairForm()

    if request.method == 'POST':

        form = RepairForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Successfully added driving records')
                return redirect('RepairTable')

            except Exception as e:
                print(e)
                messages.success(request, 'Exception:'+e)

        else:
             print(form.errors)
             messages.success(request, 'Invalid Details')


    #assign form
    var = {'repairForm': form}

    return render(request, 'Transport_templates/VehicleRepairs.html', var)



def ShowVehicleRepairs(request):

    repairs = Services.objects.all()

    return render(request, 'Transport_templates/RepairTable.html', {'repairs': repairs})


# display repairs

def DisplayUpdateRepairs(request):

    if request.method == 'POST':

        id = request.POST.get('ReId')

        if id is not None:
            try:
                repair = Services.objects.get(pk=id)
                rForm = RepairForm(instance=repair)
                return render(request, 'Transport_templates/EditRepairs.html', {'REform': rForm, 'ReId':id})

            except Exception as e:
                print(e)

        else:
            pass

    else:
        pass

    return redirect('RepairTable')



# update vehicle repairs

def UpdateVehicleRepairs(request):


    if request.method == 'POST':
        id = request.POST.get('repairID')

        if id is not None:

            try:
                repair = Services.objects.get(pk=id)
                form_update = RepairForm(request.POST, instance=repair)

                if form_update.is_valid():
                    form_update.save()
                    messages.success(request, 'Successfully update driver details')

                else:
                    #invalid
                    pass

            except Exception as e:
                print(e)
                messages.success(request, 'Invalid Details')

        else:
            #id not found
            pass

    return redirect('RepairTable')


# delete repair details

def delete_RepairRecords(request):

    id = request.POST.get('id')

    if request.method == 'POST' and id != None:
        repair = Services.objects.get(id=id)
        repair.delete()

    return redirect('RepairTable')


# reports


def Reports(request):

    return render(request, 'Transport_templates/transportation_Reports.html')


# generate vehicle details reports

class GenerateVehicle_RecordsPdf(View):
    def get(self, request, *args, **kwargs):

        vehicleNoInput = request.GET.get('vehicleno')
        month = request.GET.get('month')
        year = request.GET.get('year')
        vehicleNo = 0

        if len(month)== 2 and len(year)== 4:


            try:
                vehicle = Vehicle.objects.get(VehicleNo=vehicleNoInput)

                vehicleNo = vehicle.id

                records = Driving_Records.objects.filter(Date__month=month, Date__year=year , VehicleNo=vehicleNo)

                if len(records) > 0:

                    total = 0

                    for rec in records:
                        total = total + rec.Meter_Difference

                    data = {
                        'Vrecords': records,
                        'year':year,
                        'month':month,
                        'total': total,
                        }

                    pdf = render_to_pdf('Transport_templates/Vehicle_Reports.html', data)
                    return HttpResponse(pdf, content_type='application/pdf')

            except Vehicle.DoesNotExist:
                messages.error(request, 'No Data Found')
                return redirect('RecordTable')

            else:
                messages.error(request, 'Invalid Details')
                return redirect('Reports')

        else:
            messages.error(request, 'Invalid Inputs')
            return redirect('Reports')



# generate vehicle maintenance reports

class GenerateVehicle_RepairPdf(View):
    def get(self, request, *args, **kwargs):

        vehicleNoInput = request.GET.get('vehicleno')
        month = request.GET.get('month')
        year = request.GET.get('year')
        vehicleNo = 0

        if len(month)== 2 and len(year)== 4:

            try:
                vehicle = Vehicle.objects.get(VehicleNo=vehicleNoInput)
                vehicleNo = vehicle.id

                records = Services.objects.filter(Service_Date__month=month, Service_Date__year=year , VehicleNo=vehicleNo)

                if len(records) > 0:

                    total = 0

                    for rec in records:
                        total = total + rec.Amount

                    data = {
                        'Vrepairs': records,
                        'year':year,
                        'month':month,
                        'total': total,
                        }

                    pdf = render_to_pdf('Transport_templates/Maintenance_Report.html', data)
                    return HttpResponse(pdf, content_type='application/pdf')


            except Vehicle.DoesNotExist:
                messages.error(request, 'No Data Found')
                return redirect('Reports')

        else:
            messages.error(request, 'Invalid Inputs')
            return redirect('Reports')


# search

def SearchRecords(request):

    if request.method == 'POST':

        vehicleNoInput = request.POST.get('vehicleno')
        month = request.POST.get('month')
        year = request.POST.get('year')


        if len(month) == 2 and len(year) == 4:

            try:
                vehicle = Vehicle.objects.get(VehicleNo=vehicleNoInput)
                vehicleNo = vehicle.id
                records = Driving_Records.objects.filter(Date__month=month, Date__year=year, VehicleNo=vehicleNo)
                return render(request, 'Transport_templates/VehicleRecordsTable.html', {'records': records})


            except Vehicle.DoesNotExist:
                messages.error(request, 'No Data Found')
                return redirect('RecordTable')

        else:
            messages.error(request, 'Invalid Inputs')
            return redirect('RecordTable')




