from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Newuser
from ..models import Supreddeta
from ..models import Leafstock
from ..models import Paymentdata
from ..forms import updateform
from ..forms import supupdateform

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from ..utils import link_callback

def supplierReg(request):
    return render(request, 'supplierreg/supreg.html')


def supplierUpanddel(request):
    return render(request, 'supplierreg/supupanddel.html')


def supplierPayment(request):
    return render(request, 'supplierreg/suppayment.html')


def supplierAddleaf(request):
    return render(request, 'supplierreg/supaddleaf.html')


def supplierPaydetails(request):
    return render(request, 'supplierreg/suppaydetails.html')


def supplierLeafstock(request):
    return render(request, 'supplierreg/supleafstock.html')


def supplierRegdetails(request):
    return render(request, 'supplierreg/supregdetails.html')


def supplierTrial(request):
    return render(request, 'supplierreg/trial.html')


def Userreg(request):

    if request.method=='POST':
        Username=request.POST['Username']
        Emaill=request.POST['Emaill']
        Newuser(Username=Username, Emaill=Emaill).save()
        return render(request, 'supplierreg/trial.html')
    else:
        return render(request, 'supplierreg/trial.html')


def Supregdetails(request):

    if request.method == 'POST':
        Fullname = request.POST['Fullname']
        Nicno = request.POST['Nicno']
        Address = request.POST['Address']
        Dob = request.POST['Dob']
        Email = request.POST['Email']
        Contactnum = request.POST['Contactnum']
        Paymenttype = request.POST['Paymenttype']
        Bank = request.POST['Bank']
        Accountnum = request.POST['Accountnum']
        Supreddeta(Fullname=Fullname,  Nicno=Nicno, Address=Address, Dob=Dob, Email=Email,  Contactnum=Contactnum,  Paymenttype=Paymenttype, Bank=Bank, Accountnum=Accountnum).save()
        messages.success(request, 'Register Successfully!')
        return render(request, 'supplierreg/supreg.html')
    else:
        return render(request, 'supplierreg/supreg.html')


def Leafstockdetails(request):

    if request.method == 'POST':
        Suppliernicc = request.POST['Suppliernicc']
        Totalweight = request.POST['Totalweight']
        Receiveddate = request.POST['Receiveddate']
        Receivedtime = request.POST['Receivedtime']

        Leafstock(Suppliernicc=Suppliernicc, Totalweight=Totalweight,  Receiveddate=Receiveddate, Receivedtime=Receivedtime).save()
        messages.success(request, 'Stock Details Successfully Added!')
        return render(request, 'supplierreg/supaddleaf.html')
    else:
        return render(request, 'supplierreg/supaddleaf.html')


def Paymentdetails(request):
    if request.method == 'POST':
        Suppliernic = request.POST['Suppliernic']
        Supplierid = request.POST['Supplierid']
        Totalkilo  = request.POST['Totalkilo']
        Totalpayment = request.POST['Totalpayment']
        Date = request.POST['Date']
        Time = request.POST['Time']

        Paymentdata(Suppliernic=Suppliernic, Supplierid=Supplierid,  Totalkilo=Totalkilo, Totalpayment=Totalpayment, Date=Date, Time=Time).save()
        messages.success(request, 'Payment Details Successfully Added!')
        return render(request, 'supplierreg/suppayment.html')
    else:
        return render(request, 'supplierreg/suppayment.html')


def Trialread(request):
    Reg_list=Newuser.objects.all()
    return render(request, 'supplierreg/trialread.html', {'Reg_list':Reg_list})

def Regread(request):
    Reg_list=Supreddeta.objects.all()
    return render(request, 'supplierreg/supregdetails.html', {'Reg_list':Reg_list})

def Leafread(request):
    Reg_list=Leafstock.objects.all()
    return render(request, 'supplierreg/supleafstock.html', {'Reg_list':Reg_list})

def Payread(request):
    Pay_list=Paymentdata.objects.all()
    return render(request, 'supplierreg/suppaydetails.html', {'Pay_list':Pay_list})

def Supedit(request,id):
    displaysup=Supreddeta.objects.get(id=id)
    return render(request, 'supplierreg/supupanddel.html', {'Supreddeta':displaysup})

def supupdate(request,id):
    supupdate=Supreddeta.objects.get(id=id)
    form=supupdateform(request.POST,instance=supupdate)
    if form.is_valid():
        form.save()
        messages.success(request, 'Update Successfully!')
        return render(request, 'supplierreg/supupanddel.html', {'Supreddeta':supupdate})


def editeemp(request,id):
    displayemp=Newuser.objects.get(id=id)
    return render(request, 'supplierreg/update.html', {'Newuser':displayemp})

def update(request,id):
    update=Newuser.objects.get(id=id)
    form=updateform(request.POST,instance=update)
    if form.is_valid():
        form.save()
        return render(request, 'supplierreg/update.html', {'Newuser': update})


def Paydelete(request,id):
    deleteP=Paymentdata.objects.get(id=id)
    deleteP.delete()
    Pay_list=Paymentdata.objects.all()
    messages.success(request, 'Payment Details Successfully Deleted!')
    return render(request, 'supplierreg/suppaydetails.html', {'Pay_list': Pay_list})

def Trialdelete(request,id):
    deleteT=Newuser.objects.get(id=id)
    deleteT.delete()
    Reg_list=Newuser.objects.all()
    return render(request, 'supplierreg/trialread.html', {'Reg_list': Reg_list})

def Supdelete(request,id):
    deleteS=Supreddeta.objects.get(id=id)
    deleteS.delete()
    Reg_list=Supreddeta.objects.all()
    messages.success(request, 'Supplier Details Successfully Deleted!')
    return render(request, 'supplierreg/supregdetails.html', {'Reg_list': Reg_list})

def Leafdelete(request,id):
    deleteL=Leafstock.objects.get(id=id)
    deleteL.delete()
    Reg_list=Leafstock.objects.all()
    messages.success(request, 'Stock Details Successfully Deleted!')
    return render(request, 'supplierreg/supleafstock.html', {'Reg_list': Reg_list})

def generatepayment(request):
    template_path = 'supplierreg/SupPayDetailsPDF.html'
    Pay_list = Paymentdata.objects.all()
    context = {
        'Pay_list': Pay_list
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="PaymentD.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

