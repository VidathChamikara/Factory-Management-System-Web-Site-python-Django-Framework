import datetime
import pytz
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from ..forms import AddProductPriceForm, AddItemToCart, AddBill, AddBillProduct, Stock, CategoryProduct, ProductPrice
from ..forms import Cart, Bill, BillProduct, DeletedProduct

# TO GENERATE PDF
from django.http import HttpResponse
from django.views.generic import View
from ..utils import render_to_pdf

loginUrl = '/admin/login/'


# ----------------------------------------- PRICE TABLE -----------------------------------------
@login_required(login_url=loginUrl)
def sales_price_table(request):
    price = ProductPrice.objects.all()
    product = CategoryProduct.objects.all().order_by('cp_name', 'category', 'weight')
    form = AddProductPriceForm()

    # get only the products that are not in the price table
    ppriceid = [proid.product_id for proid in price]
    addproduct = CategoryProduct.objects.exclude(id__in=ppriceid).order_by('cp_name', 'category', 'weight')

    if request.method == 'POST':
        try:
            productid = request.POST.get('product')
            productprice = request.POST.get('poductprice')
            formdata = {'product': int(productid),
                        'product_price': float(productprice),
                        }
            if float(productprice) > 0:
                # check the item already in the list
                product_chk = ProductPrice.objects.filter(product_id=productid)
                form = AddProductPriceForm(formdata)

                if product_chk:
                    messages.warning(request, 'Product price already added to the list.')
                else:
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Product successfully added to the list.')

            else:
                messages.error(request, 'Invalid data!')

        except Exception as e:
            print(e)
            messages.error(request, 'Invalid data!')

        return redirect('/Shop/Outlet/priceTable/')
    else:
        # search bar option
        if 'search' in request.GET:
            search = request.GET['search']
            product = CategoryProduct.objects.filter(
                Q(id__icontains=search) | Q(cp_name__icontains=search) | Q(category__icontains=search) |
                Q(weight__icontains=search)).order_by('cp_name', 'category', 'weight')
            messages.info(request, 'Search results...')

        template = 'Outlet_Sales/priceTable.html'
        context = {'Product': product, 'price': price, 'form': form, 'addProduct': addproduct}
        return render(request, template, context)


@login_required(login_url=loginUrl)
def update_product_price(request):
    if request.method == 'POST':
        productid = request.POST.get('editid')
        newprice = request.POST.get('editprice')

        try:
            if float(newprice) >= 0:
                product = ProductPrice.objects.get(product_id=productid)

                product.product_price = newprice
                product.save()

                messages.info(request, 'Price successfully updated!')
            else:
                messages.error(request, 'Price could not be minus(-) !')

        except Exception as e:
            print(e)
            messages.error(request, 'Invalid data!')

    return redirect('/Shop/Outlet/priceTable/')


@login_required(login_url=loginUrl)
def remove_product_price(request):
    if request.method == 'POST':
        try:
            productid = request.POST.get('deleteidpass')
            product = ProductPrice.objects.get(product_id=productid)
            product.delete()
            messages.info(request, 'Successfully Deleted!')

        except Exception as e:
            print(e)
            messages.error(request, 'Invalid data!')

    return redirect('/Shop/Outlet/priceTable/')


# ------------------------------------------- NEW BILL --------------------------------------------
class SubTotals:
    def __init__(self, id, subTol):
        self.id = id
        self.subTol = subTol


@login_required(login_url=loginUrl)
def new_bill(request):
    price = ProductPrice.objects.all()
    product = CategoryProduct.objects.all().order_by('cp_name', 'category', 'weight')
    cart = Cart.objects.all()
    form = AddItemToCart()

    if request.method == 'POST':
        try:
            productid = request.POST.get('product')
            qty = request.POST.get('qty')

            # check qty is only white spaces or empty
            if qty.isspace() or not qty:
                qty = 1

            formdata = {'product': int(productid),
                        'QTY': int(qty),
                        }

            if int(qty) > 0:
                # check the item already in the list
                product_chk = Cart.objects.filter(product_id=productid)
                form = AddItemToCart(formdata)

                if product_chk:
                    messages.warning(request, 'Item already added to the list.')
                else:
                    product = CategoryProduct.objects.get(id=productid)
                    stock = Stock.objects.filter(Q(category=product.category) & Q(weight=product.weight))
                    if stock:
                        stock = Stock.objects.get(Q(category=product.category) & Q(weight=product.weight))

                        if int(stock.available_stock) > 0:
                            if int(stock.available_stock) >= int(qty):
                                if form.is_valid():
                                    form.save()
                                    messages.success(request, 'Item successfully added to the list.')
                                else:
                                    messages.error(request, 'Invalid data!')
                            else:
                                msg = 'Available stock: ' + str(stock.available_stock)
                                messages.warning(request, msg)
                        else:
                            messages.error(request, 'No stock available!')
                    else:
                        messages.error(request, 'No stock available!')

            else:
                messages.error(request, 'Invalid data!')

        except Exception as e:
            print(e)
            messages.error(request, 'Invalid data!')

        return redirect('/Shop/Outlet/newBill/')
    else:
        # get the sub total of an item as for the quantity and the bill total
        sub_total_list = []
        bill_total = 0
        for prod in product:
            for item in cart:
                for pri in price:
                    if prod.id == item.product_id and prod.id == pri.product_id:
                        sub_t = round(pri.product_price * item.QTY, 2)
                        sub_total_list.append(SubTotals(prod.id, sub_t))
                        bill_total += sub_t

        template = 'Outlet_Sales/newBill.html'
        context = {'Product': product, 'price': price, 'cart': cart, 'form': form, 'subTotal': sub_total_list,
                   'billTotal': round(bill_total, 2)}
        return render(request, template, context)


@login_required(login_url=loginUrl)
def update_cart(request):
    if request.method == 'GET':
        product_id = request.GET.get('updateItemId')
        product = Cart.objects.get(product_id=product_id)

        try:
            # check which button is selected
            if request.GET.get("decreaseQTY"):
                product.QTY -= 1

                if product.QTY < 1:
                    messages.warning(request, 'QTY cannot be less than 1!')
                else:
                    product.save()

            elif request.GET.get("increaseQTY"):
                product.QTY += 1
                select_product = CategoryProduct.objects.get(id=product_id)
                stock = Stock.objects.get(Q(category=select_product.category) & Q(weight=select_product.weight))
                if stock.available_stock < product.QTY:
                    msg = 'Available stock: ' + str(stock.available_stock)
                    messages.warning(request, msg)
                else:
                    product.save()

        except Exception as e:
            print(e)
            messages.error(request, 'Invalid data!')

    return redirect('/Shop/Outlet/newBill/')


@login_required(login_url=loginUrl)
def remove_from_cart(request):
    if request.method == 'POST':
        try:
            productid = request.POST.get('deleteidpass')
            item = Cart.objects.get(product_id=productid)
            item.delete()
            messages.info(request, 'Item removed from cart!')

        except Exception as e:
            print(e)
            messages.error(request, 'Invalid data!')

    return redirect('/Shop/Outlet/newBill/')


@login_required(login_url=loginUrl)
def clear_cart(request):
    cart = Cart.objects.all()

    for item in cart:
        item.delete()

    messages.info(request, 'Cart is clear!')

    return redirect('/Shop/Outlet/newBill')


@login_required(login_url=loginUrl)
def checkout(request):
    if request.method == "POST":
        try:
            cart = Cart.objects.all()
            if cart:
                bill_amount = request.POST.get('totalAmount')
                given_cash = request.POST.get('givenCash')
                time = datetime.datetime.now(pytz.timezone('Asia/Colombo')).time()
                date = datetime.datetime.now().date()

                if float(bill_amount) > float(given_cash):
                    messages.error(request, 'Given cash amount is less than the bill amount...')
                else:
                    bill_form_data = {'Total_amount': float(bill_amount),
                                      'Given_cash_amount': float(given_cash),
                                      'Time': time,
                                      'Date': date,
                                      'Handled_by': request.user.get_full_name(),
                                      }
                    bii_form = AddBill(bill_form_data)

                    if bii_form.is_valid():
                        bii_form.save()

                        # get the bill id to add products to the bill products table
                        bill_id = Bill.objects.last().id

                        # add item to the bill product table from cart table
                        for item in cart:
                            price = ProductPrice.objects.get(product_id=item.product_id).product_price
                            bill_product_form_data = {'Bill_Number': bill_id,
                                                      'Product': item.product_id,
                                                      'Price': price,
                                                      'QTY': item.QTY,
                                                      }
                            bill_product_form = AddBillProduct(bill_product_form_data)

                            if bill_product_form.is_valid():
                                bill_product_form.save()

                                # decrease the QTY from available stock
                                select_product = CategoryProduct.objects.get(id=item.product_id)
                                stock = Stock.objects.get(
                                    Q(category=select_product.category) & Q(weight=select_product.weight))
                                stock.available_stock -= item.QTY
                                stock.save()
                                # remove added item from cart
                                item.delete()

                        # calculate the balance that wants to give back to the customer
                        balance = "Payment successful!  Balance is - Rs." + str(
                            round(float(given_cash) - float(bill_amount), 2))
                        messages.success(request, balance)
                        return redirect('bill-details', id=bill_id)

                    else:
                        messages.error(request, 'Invalid data!')

            else:
                messages.error(request, 'No item to checkout!')

        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred!')

    return redirect('/Shop/Outlet/newBill')


# ------------------------------------------- TRANSACTIONS --------------------------------------------
@login_required(login_url=loginUrl)
def transactions(request):
    bill = Bill.objects.all().order_by('-id')

    # search transactions by bill number or date
    if request.method == 'POST':
        if 'search' or 'dateSearch' in request.POST:
            try:
                search = request.POST['search']

                # check search is only white spaces or empty
                if search.isspace() or not search:
                    search = request.POST['dateSearch']
                    if search.isspace() or not search:
                        messages.error(request, 'Enter bill number or select the date to search...')
                    else:
                        bill = Bill.objects.filter(Date=search).order_by('-id')
                        if not bill:
                            messages.error(request, 'No result found!')
                        else:
                            messages.info(request, 'Search results...')
                else:
                    bill = Bill.objects.filter(Q(id=search)).order_by('-id')
                    if not bill:
                        messages.error(request, 'No result found!')
                    else:
                        messages.info(request, 'Search results...')

            except Exception as e:
                print(e)
                messages.error(request, 'An error occurred!')

    template = 'Outlet_Sales/transactionList.html'
    context = {'Bills': bill}
    return render(request, template, context)


@login_required(login_url=loginUrl)
def view_bill_details(request, id):
    try:
        if request.method == 'POST':
            select_id = request.POST['bill_id']
        else:
            select_id = id
        bill = Bill.objects.get(id=select_id)
        balance = bill.Given_cash_amount - bill.Total_amount
        bill_products = BillProduct.objects.filter(Bill_Number_id=select_id)
        product_details = []
        sub_total_list = []
        for products in bill_products:
            try:
                product = CategoryProduct.objects.get(id=products.Product)
            except Exception as e:
                print(e)
                product = DeletedProduct.objects.get(id=products.Product)
            product_details.append(product)
            sub_t = round(products.Price * products.QTY, 2)
            sub_total_list.append(SubTotals(products.Product, sub_t))

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred!')
        return redirect('/Shop/Outlet/transactions')

    template = 'Outlet_Sales/billDetailView.html'
    context = {'Bill': bill, 'Balance': round(balance, 2), 'Bill_products': bill_products,
               'Bill_product_details': product_details, 'Sub_total': sub_total_list}
    return render(request, template, context)


@login_required(login_url=loginUrl)
def delete_bill_details(request):
    if request.method == 'POST':
        try:
            bill_id = request.POST.get('deleteBillIDPass')
            bill = Bill.objects.get(id=bill_id)
            bill_product_list = BillProduct.objects.filter(Bill_Number_id=bill_id)
            bill.delete()
            for product in bill_product_list:
                product.delete()
            messages.info(request, 'Bill records successfully deleted!')
        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred!')

    return redirect('transactions')


# ------------------------------------------- SALES REPORTS --------------------------------------------
@login_required(login_url=loginUrl)
def sales_reports(request):
    try:
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        if month == 1:
            last_year = year - 1
            last_month = 12
        else:
            last_year = year
            last_month = month - 1

        # retrieve sales data for this month and last month
        this_month_db_data = Bill.objects.filter(
            Q(Date__month=month) & Q(Date__year=year)
        )
        last_month_db_data = Bill.objects.filter(
            Q(Date__month=last_month) & Q(Date__year=last_year)
        )

        # arrange data for the line chart
        line_chart_data_list = []
        this_day_sales = 0
        last_day_sales = 0
        for this_day in range(1, 32):
            for data in this_month_db_data:
                if data.Date.day == this_day:
                    this_day_sales += data.Total_amount
            for data in last_month_db_data:
                if data.Date.day == this_day:
                    last_day_sales += data.Total_amount

            data_array = [str(this_day), last_day_sales, this_day_sales]
            line_chart_data_list.append(data_array)
            this_day_sales = 0
            last_day_sales = 0

        # arrange data for this month pie chart
        bill_id_list = []
        for bill in this_month_db_data:
            bill_id_list.append(bill.id)

        # Get the products and each of their counts in the bill id list
        products_in_bill = BillProduct.objects.values('Product')\
            .annotate(count=Sum('QTY')).filter(Bill_Number_id__in=bill_id_list)

        products_in_bill = list(products_in_bill.values_list('Product', 'count'))

        this_month_pie = []
        for products in products_in_bill:
            product = CategoryProduct.objects.get(id=products[0])
            data_array = [str(product.cp_name)+' '+str(product.weight), products[1]]
            this_month_pie.append(data_array)

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred!')
        return redirect('price-table')

    template = 'Outlet_Sales/salesReports.html'
    context = {'LineData': line_chart_data_list, 'ThisMonthPie': this_month_pie}
    return render(request, template, context)


