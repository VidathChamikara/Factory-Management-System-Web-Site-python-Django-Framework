from django.shortcuts import render
from django.contrib import messages
from ..models import Newuser
from ..models import buyers
from ..models import auction
from ..models import soldStock
from ..models import notsoldStock
from ..forms import updateform
from ..forms import updateBuyerform
from ..forms import updateAuctionform



# TO GENERATE PDF
#from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
#from django.views.generic import View
#from ..utils import render_to_pdf
from ..utils import link_callback


def Userreg(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        Email = request.POST['Email']
        Newuser(Username=Username, Email=Email).save()
        return render(request, 'auctionStocks/Registration.html')
    else:
        return render(request, 'auctionStocks/Registration.html')


def RegRead(request):
    Reg_list = Newuser.objects.all()
    return render(request, 'auctionStocks/RegistrationRead.html', {'Reg_list': Reg_list})


def editemp(request, id):
    displayemp = Newuser.objects.get(id=id)
    return render(request, 'auctionStocks/UpdateRegistration.html', {'Newuser': displayemp})


def updateemp(request, id):
    updateemp = Newuser.objects.get(id=id)
    form = updateform(request.POST, instance=updateemp)
    if form.is_valid():
        form.save()
    return render(request, 'auctionStocks/UpdateRegistration.html', {'Newuser': updateemp})


def AddNewBuyer(request):
    if request.method == 'POST':
        Cname = request.POST['Cname']
        regNo = request.POST['regNo']
        Address = request.POST['Address']
        PNumber = request.POST['PNumber']
        buyers(Cname=Cname, regNo=regNo, Address=Address, PNumber=PNumber).save()
        messages.success(request,'Record Saved Successfully...!')
        return render(request, 'auctionStocks/AddNewBuyer.html')
    else:
        return render(request, 'auctionStocks/AddNewBuyer.html')


def BuyerRead(request):
    buyerDetails = buyers.objects.all()
    return render(request, 'auctionStocks/BuyerDetails.html', {'buyerDetails': buyerDetails})


def editBuyer(request, id):
    displayBuyers = buyers.objects.get(id=id)
    return render(request, 'auctionStocks/UpdateBuyer.html', {'buyers': displayBuyers})


def updateBuyer(request, id):
    updateB = buyers.objects.get(id=id)
    form = updateBuyerform(request.POST, instance=updateB)
    if form.is_valid():
        form.save()
    messages.success(request, 'Record Updated Successfully...!')
    return render(request, 'auctionStocks/UpdateBuyer.html', {'buyers': updateB})


def deleteBuyer(request, id):
    deleteB = buyers.objects.get(id=id)
    deleteB.delete()
    buyerDetails = buyers.objects.all()
    return render(request, 'auctionStocks/BuyerDetails.html', {'buyerDetails': buyerDetails})


def addAuction(request):
    if request.method == 'POST':
        stockID = request.POST['stockID']
        teacat = request.POST['teacat']
        totWeight = request.POST['totWeight']
        packages = request.POST['packages']
        datePrepared = request.POST['datePrepared']
        auction(stockID=stockID, teacat=teacat, totWeight=totWeight, packages=packages,
                datePrepared=datePrepared).save()
        messages.success(request, 'Record Saved Successfully...!')
        return render(request, 'auctionStocks/PrepareCatelog.html')
    else:
        return render(request, 'auctionStocks/PrepareCatelog.html')


def readAuction(request):
    auctionDetails = auction.objects.all()
    return render(request, 'auctionStocks/AllCatelog.html', {'auctionDetails': auctionDetails})


def editAuction(request, id):
    displayAuction = auction.objects.get(id=id)
    return render(request, 'auctionStocks/UpdateAuction.html', {'auction': displayAuction})


def updateAuction(request, id):
    updateA = auction.objects.get(id=id)
    form = updateAuctionform(request.POST, instance=updateA)
    if form.is_valid():
        form.save()
    messages.success(request, 'Record Updated Successfully...!')
    return render(request, 'auctionStocks/UpdateAuction.html', {'auction': updateA})


def deleteAuction(request, id):
    deleteB = auction.objects.get(id=id)
    deleteB.delete()
    auctionDetails = auction.objects.all()
    return render(request, 'auctionStocks/AllCatelog.html', {'auctionDetails': auctionDetails})


def readStock(request):
    auctionDetails = auction.objects.all()
    return render(request, 'stockSales/currentStock.html', {'auctionDetails': auctionDetails})




def editStock(request, id):
    displayStock = auction.objects.get(id=id)
    return render(request, 'stockSales/soldStock.html', {'auction': displayStock})


def SoldStock(request, id):
    if request.method == 'POST':
        stockID = request.POST['stockID']
        teacat = request.POST['teacat']
        totWeight = request.POST['totWeight']
        packages = request.POST['packages']
        datePrepared = request.POST['datePrepared']
        Cname = request.POST['Cname']
        regNo = request.POST['regNo']
        soldStock(stockID=stockID, teacat=teacat, totWeight=totWeight, packages=packages, datePrepared=datePrepared,
                  Cname=Cname, regNo=regNo).save()
        messages.success(request, 'Record Saved Successfully...!')
    return render(request, 'stockSales/soldStock.html')


def readSoldStock(request):
    soldStockDetails = soldStock.objects.all()
    return render(request, 'stockSales/readSoldStock.html', {'soldStockDetails': soldStockDetails})


def editnotSoldStock(request, id):
    displayNotSoldStock = auction.objects.get(id=id)
    return render(request, 'stockSales/notsoldStock.html', {'auction': displayNotSoldStock})


def notSoldStock(request, id):
    if request.method == 'POST':
        stockID = request.POST['stockID']
        teacat = request.POST['teacat']
        totWeight = request.POST['totWeight']
        packages = request.POST['packages']
        datePrepared = request.POST['datePrepared']
        notsoldStock(stockID=stockID, teacat=teacat, totWeight=totWeight, packages=packages,
                     datePrepared=datePrepared).save()
        messages.success(request, 'Record Saved Successfully...!')
    return render(request, 'stockSales/notsoldStock.html')


def readnotSoldStock(request):
    notsoldStockDetails = notsoldStock.objects.all()
    return render(request, 'stockSales/readnotSoldStock.html', {'notsoldStockDetails': notsoldStockDetails})


def deleteCurrentStock(request, id):
    deleteB = auction.objects.get(id=id)
    deleteB.delete()
    auctionDetails = auction.objects.all()
    return render(request, 'stockSales/currentStock.html', {'auctionDetails': auctionDetails})




# -------------------PDF-------------------------------------


#def BuyerReadPDF(request):
#    buyerDetails = buyers.objects.all()
#    return render(request, 'auctionStocks/BuyerDetailsPDF.html', {'buyerDetails': buyerDetails})



def generateReport(request):
    template_path = 'auctionStocks/BuyerDetailsPDF.html'
    buyerDetails = buyers.objects.all()
    context = {
        'buyerDetails': buyerDetails
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="BuyerD.pdf"'
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

def generateReportStock(request):
    template_path = 'stockSales/currentStockPDF.html'
    auctionDetails = auction.objects.all()
    context = {
        'auctionDetails': auctionDetails
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Current Stock.pdf"'
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




# def editBuyerPDF(request,id):
#    displayBuyers=buyers.objects.get(id=id)
#    return render(request, 'auctionStocks/BuyerDetailsPDF.html',{'buyers':displayBuyers})
#
# def GeneratePDF(request,id):
#
#    if request.method=='POST':
#        Cname=request.POST['Cname']
#        regNo=request.POST['regNo']
#        Address = request.POST['Address']
#        PNumber = request.POST['PNumber']
#        buyers(Cname=Cname, regNo=regNo, Address=Address, PNumber=PNumber).save()
#        pdf = render_to_pdf('auctionStocks/BuyerDetailsPDF.html')
#    return HttpResponse(pdf, content_type='application/pdf')


#class generateReport(View):
#    def get(self, request, *args, **kwargs):
#        context = {
#                'buyers': buyerDetails
#            }
#        pdf = render_to_pdf('auctionStocks/BuyerDetailsPDF.html', context)
#        if pdf:
#            response = HttpResponse(pdf, content_type='application/pdf')
#            return response
#        return HttpResponse("Not found")


# ---------------------------------------------------------------------------------
def addSubStock(request):
    return render(request, 'auctionStocks/AddSubStock.html')


def allcat(request):
    return render(request, 'auctionStocks/AllCatelog.html')


def preparecat(request):
    return render(request, 'auctionStocks/PrepareCatelog.html')


def Indexpage(request):
    return render(request, 'auctionStocks/index.html')
