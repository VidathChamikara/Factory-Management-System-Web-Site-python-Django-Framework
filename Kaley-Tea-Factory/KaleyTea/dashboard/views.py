from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm, OrderForm, AddTeaGradeform, AddMainProductForm, AddSubProductForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Order, Final_product_sub, Final_product_Main, TeaGrades
from FactorySystem.utils import render_to_pdf


# Create your views here.
# --------------------------Create Inventory Dashboard----------------------------------
@login_required()
def index(request):
    return render(request, 'dashboard/index.html')


# --------------------------Create Inventory Add----------------------------------

@login_required()
def product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Inventory details saved successfully')
                return redirect('dashboardProductView')
            except:
                pass

        else:
            messages.error(request, "Invalid Details")

    context = {
        'form': form,
    }
    return render(request, 'dashboard/product.html', context)


# ----------------------------Create Inventory View---------------------------------

@login_required()
def product_view(request):
    leaf = Product.objects.all()
    return render(request, 'dashboard/product_view.html', {'leaf': leaf})


# ----------------------------Create Inventory Update---------------------------------

@login_required()
def product_update(request):
    if request.method == 'POST':
        inv_ID = request.POST.get('lid')

        if inv_ID:

            try:
                item = Product.objects.get(id=inv_ID)
                form = ProductForm(request.POST, instance=item)
                return render(request, 'dashboard/product_update.html', {'form': form, 'lid': inv_ID})

            except Exception as e:
                print(e)
        else:
            messages.error(request, "Inv id is null")

    else:
        # id is null
        pass

    return redirect('dashboard/product_view.html')


@login_required()
def updateLeaf(request):
    if request.method == 'POST':
        leafID = request.POST.get('LID')

        if leafID is not None:

            try:
                item = Product.objects.get(pk=leafID)
                form = ProductForm(request.POST, instance=item)

                if form.is_valid():
                    form.save()

                    return redirect('/product/view')

                else:
                    messages.error(request, "Invalid Details")

            except Exception as e:
                print(e)

        else:
            # id is null
            pass

    return redirect('/product/view')


@login_required()
def NavigateToPrevInv(request):
    item = Product.objects.all()
    return render(request, 'dashboard/product_view.html', {'item': item})


@login_required(login_url='login')
def NavigateToPrevInv(request):
    leaf = Product.objects.all()
    return render(request, 'LeafInventory_templates/View_pre_inv.html', {'leaf': leaf})


@login_required(login_url='login')
def NavigateToUpdateInv(request):
    if request.method == 'POST':
        inv_ID = request.POST.get('lid')

        if inv_ID is not None:
            try:
                item = Product.objects.get(id=inv_ID)
                form = ProductForm(instance=item)
                return render(request, 'dashboard/product_update.html', {'form': form, 'lid': inv_ID})

            except Exception as e:
                print(e)

        else:
            messages.error(request, "Inv id is null")

    else:
        # method is not post
        pass

    return render(request, 'dashboard/product_view.html')


# ---------------------------Create Inventory Delete---------------------------------

@login_required()
def product_delete(request):
    leafid = request.POST.get('leafid')
    if request.method == 'POST':
        leaf = Product.objects.get(id=leafid)
        leaf.delete()
        return redirect('dashboardProductView')
    return render(request, '/product/view')


# -------------------------Create Inventory Report File-----------------------------

@login_required()
def NavigateToInvReport(request):
    if request.method == 'POST':
        leafID = request.POST.get('leafID')

        item = Product.objects.get(id=leafID)

        context = {
            'item': item,
        }

        pdf = render_to_pdf('dashboard/inventoryPDF.html', context)

        return HttpResponse(pdf, content_type='application/pdf')

    return redirect('/product/view/')


# --------------------------Create Inventory Staff View----------------------------------
@login_required()
def staff(request):
    workers = User.objects.all()
    context = {
        'workers': workers
    }
    return render(request, 'dashboard/staff.html', context)


# ---------------------------Create Order Form---------------------------------

@login_required()
def order(request):
    orders = Order.objects.all()

    context = {
        'orders': orders
    }

    return render(request, 'dashboard/order.html', context)


# ---------------------------Create Search Bar Form---------------------------------
@login_required()
def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        item = Product.objects.all().filter(tray_id=search)
        return render(request, 'dashboard/searchbar.html', {'item': item})


def make_request(request):
    orders = User.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-order')
    else:
        form = OrderForm()
    context = {
        'orders': orders,
        'form': form,
    }
    return render(request, 'dashboard/make_request.html', context)


# ----------------------------------------------------------------------------------------------------------------------


# --------------------------------- Inventory Daily Production Management -----------------------------------
@login_required()
def NavigateToProduction(request):
    form = AddSubProductForm()
    mFrom = AddMainProductForm()
    genID = 0

    # generate sub id
    mainProduct = Final_product_Main.objects.last()

    if mainProduct is not None:
        genID = mainProduct.subID + 1
    else:
        genID = 1

    if request.method == 'POST':

        form = AddSubProductForm(request.POST)

        if form.is_valid():

            try:
                productObj = form.save(commit=False)
                productObj.subID = genID
                productObj.save()

                messages.success(request, 'Successfully Added')
                return redirect('final_production_home')

            except Exception as e:
                print(e)
                messages.error(request, 'Exception')

        else:
            print(form.errors)
            messages.error(request, 'Invalid Details')

    # get subfinal production details
    subFinal = Final_product_sub.objects.filter(subID=genID)

    var = {'form': form,
           'mainForm': mFrom,
           'subID': genID,
           'finalSubProduct': subFinal
           }

    return render(request, 'dashboard/Add_daily_product.html', var)


@login_required()
def addMainFinalProduction(request):
    if request.method == 'POST':
        sid = request.POST.get('sID')

        # calculate total weight
        total = 0
        allProduct = Final_product_sub.objects.filter(subID=sid)

        for product in allProduct:
            total = total + product.gradeWeight

        form = AddMainProductForm(request.POST)

        if form.is_valid():
            mainObj = form.save(commit=False)
            mainObj.subID = sid
            mainObj.totalWeight = total
            mainObj.save()

            messages.success(request, "Successfully Saved Data")
            return redirect('NavigateToCustomDailyProd')

        else:
            messages.error(request, "invalid")

    return redirect('final_production_home')


@login_required()
def deleteSubProd(request):
    if request.method == 'POST':
        sID = request.POST.get('id')

        if sID is not None:

            try:
                subProd = Final_product_sub.objects.get(id=sID)

                # update main prod
                mainProdID = subProd.subID
                mainProd = Final_product_Main.objects.get(subID=mainProdID)

                mainProd.totalWeight = mainProd.totalWeight - subProd.gradeWeight
                mainProd.save()

                # delete sub prod
                subProd.delete()

                subProuctChk = Final_product_sub.objects.filter(subID=mainProdID)

                if len(subProuctChk) < 1:
                    mainProd.delete()

                messages.success(request, 'Successfully Deleted')
                return redirect('NavigateToCustomDailyProd')

            except Exception as e:
                print(e)

    return redirect('NavigateToCustomDailyProd')


@login_required()
def NavigateToCustomDailyProd(request):
    prod = Final_product_Main.objects.all()
    return render(request, 'dashboard/View_Daily_production.html', {'prod': prod})


@login_required()
def NavigateToViewProduct(request):
    if request.method == 'POST':
        sid = request.POST.get('id')

        product = Final_product_sub.objects.filter(subID=sid)
        mainProd = Final_product_Main.objects.get(subID=sid)
        date = mainProd.date

    return render(request, 'dashboard/sub_final_product_view.html', {'products': product, 'date': date})


def NavigateToDelSubPr(request):
    spr = request.POST.get('spr')

    if request.method == 'POST' and spr is not None:
        subpro = Final_product_sub.objects.get(id=spr)
        subpro.delete()

    return redirect('final_production_home')


def NavigateToTeaGrades(request):
    form = AddTeaGradeform()
    if request.method == 'POST':
        form = AddTeaGradeform(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Tea grade Saved successfully')
                return redirect('NavigateToTeaGrades')
            except:
                pass

    grade = TeaGrades.objects.all()

    var = {'form': form,
           'grade': grade}

    return render(request, 'dashboard/TeaGrades.html', var)


def DeleteGrade(request):
    grade = request.POST.get('grade')

    if request.method == 'POST' and grade is not None:
        gradeT = TeaGrades.objects.get(id=grade)
        gradeT.delete()

    return redirect('NavigateToTeaGrades')
