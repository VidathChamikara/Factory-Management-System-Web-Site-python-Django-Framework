# ---------------------------------- GENERATE PDFs --------------------------------------------
from datetime import datetime, timedelta
import pathlib
import io

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from FactorySystem.models import Bill, BillProduct, CategoryProduct, DeletedProduct
from FactorySystem.utils import render_to_pdf
from FactorySystem.view_mappings.outletSalesViews import loginUrl, SubTotals


def get_max(arr):
    n = len(arr)
    max_num = arr[0]
    for i in range(1, n):
        if arr[i] > max_num:
            max_num = arr[i]
    return max_num


@login_required(login_url=loginUrl)
def generate_bill(request, id):
    if request.method == 'POST':
        bill_id = request.POST['billIDPass']
    else:
        bill_id = id

    try:
        bill = Bill.objects.get(id=bill_id)
        balance = bill.Given_cash_amount - bill.Total_amount
        bill_products = BillProduct.objects.filter(Bill_Number_id=bill_id)
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

    data = {'Bill': bill,
            'Balance': round(balance, 2),
            'Bill_products': bill_products,
            'Bill_product_details': product_details,
            'Sub_total': sub_total_list
            }
    pdf = render_to_pdf('Outlet_Sales/PDF/bill.html', data)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        return response
    return HttpResponse("Not found")


@login_required(login_url=loginUrl)
def report_yesterday(request):
    try:
        raw_yesterday = datetime.now() - timedelta(1)
        yesterday = datetime.strftime(raw_yesterday, '%Y-%m-%d')

        report_for = datetime.strftime(raw_yesterday, '%b. %d, %Y')
        generated_on = datetime.now()
        generated_by = request.user.get_full_name()

        yesterday_bills = Bill.objects.filter(Date=yesterday)
        if not yesterday_bills:
            messages.info(request, 'No reports for '+str(yesterday))
            return redirect('sales-reports')

        bill_id_list = []
        total_sales = 0
        bill_count = 0
        # Calculate the total sales
        for bill in yesterday_bills:
            bill_id_list.append(bill.id)
            total_sales += bill.Total_amount
            bill_count += 1

        # Get the products and each of their counts in the bill id list
        products_in_bill = BillProduct.objects.values('Product', 'Price')\
            .annotate(count=Sum('QTY')).filter(Bill_Number_id__in=bill_id_list)

        # Calculate the total items sold
        total_items = 0
        product_qty_arr = []
        for product in products_in_bill:
            total_items += product.get('count')
            product_qty_arr.append(product.get('count'))

        # Get the most sold item
        max_num = get_max(product_qty_arr)
        most_sold = []
        for data in products_in_bill:
            if data.get('count') == max_num:
                product = CategoryProduct.objects.get(id=data.get('Product'))
                most_sold.append(str(product.cp_name))
        # If the most sold items are greater than 2
        if len(most_sold) > 2:
            most_sold.clear()
            most_sold.append('(Have many items)')

        # Arrange data for the charts
        products_in_bill = list(products_in_bill.values_list('Product', 'Price', 'count'))
        chart_data_list = []
        chart_data_list2 = []
        for data in products_in_bill:
            product = CategoryProduct.objects.get(id=data[0])
            data_array = [str(product.cp_name), data[2]]
            data_array2 = [str(product.cp_name), data[1] * data[2]]
            chart_data_list.append(data_array)
            chart_data_list2.append(data_array2)

        # Calculate average price per bill
        average_price = total_sales/bill_count

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred!')
        return redirect('sales-reports')

    template = 'Outlet_Sales/PDF/salesReportTemplate.html'
    context = {'ChartData': chart_data_list,
               'ChartData2': chart_data_list2,
               'ReportFor': report_for,
               'GeneratedOn': generated_on,
               'GeneratedBy': generated_by,
               'TotalSales': total_sales,
               'TotalItems': total_items,
               'MostSold': most_sold,
               'NoOfBills': bill_count,
               'AveragePrice': average_price,
               }
    return render(request, template, context)


@login_required(login_url=loginUrl)
def report_last_7_days(request):
    try:
        days_list = []

        for i in range(1, 8):
            row_get_date = datetime.now() - timedelta(i)
            get_date = datetime.strftime(row_get_date, '%Y-%m-%d')
            days_list.append(get_date)

        raw_yesterday = datetime.now() - timedelta(1)
        yesterday = datetime.strftime(raw_yesterday, '%Y-%m-%d')

        raw_before_7_days = datetime.now() - timedelta(7)
        before_7_days = datetime.strftime(raw_before_7_days, '%Y-%m-%d')

        report_for = before_7_days + ' to ' + yesterday
        generated_on = datetime.now()
        generated_by = request.user.get_full_name()

        bills = Bill.objects.filter(Date__in=days_list)
        if not bills:
            messages.info(request, 'No reports for last 7 days!')
            return redirect('sales-reports')

        bill_id_list = []
        total_sales = 0
        bill_count = 0
        # Calculate the total sales
        for bill in bills:
            bill_id_list.append(bill.id)
            total_sales += bill.Total_amount
            bill_count += 1

        # Get the products and each of their counts in the bill id list
        products_in_bill = BillProduct.objects.values('Product')\
            .annotate(count=Sum('QTY')).filter(Bill_Number_id__in=bill_id_list)

        # Calculate the total items sold
        total_items = 0
        product_qty_arr = []
        for product in products_in_bill:
            total_items += product.get('count')
            product_qty_arr.append(product.get('count'))

        # Get the most sold item
        max_num = get_max(product_qty_arr)
        most_sold = []
        for data in products_in_bill:
            if data.get('count') == max_num:
                product = CategoryProduct.objects.get(id=data.get('Product'))
                most_sold.append(str(product.cp_name))
        # If the most sold items are greater than 2
        if len(most_sold) > 2:
            most_sold.clear()
            most_sold.append('(Have many items)')

        # Arrange data for the charts
        products_in_bill = list(products_in_bill.values_list('Product', 'Price', 'count'))
        chart_data_list = []
        chart_data_list2 = []
        for data in products_in_bill:
            product = CategoryProduct.objects.get(id=data[0])
            data_array = [str(product.cp_name), data[2]]
            data_array2 = [str(product.cp_name), data[1] * data[2]]
            chart_data_list.append(data_array)
            chart_data_list2.append(data_array2)

        # Calculate average price per bill
        average_price = round(total_sales/bill_count, 2)

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred!')
        return redirect('sales-reports')

    template = 'Outlet_Sales/PDF/salesReportTemplate.html'
    context = {'ChartData': chart_data_list,
               'ChartData2': chart_data_list2,
               'ReportFor': report_for,
               'GeneratedOn': generated_on,
               'GeneratedBy': generated_by,
               'TotalSales': total_sales,
               'TotalItems': total_items,
               'MostSold': most_sold,
               'NoOfBills': bill_count,
               'AveragePrice': average_price,
               }
    return render(request, template, context)


@login_required(login_url=loginUrl)
def report_last_month(request):
    try:
        month = datetime.now().month
        year = datetime.now().year
        if month == 1:
            last_year = year - 1
            last_month = 12
        else:
            last_year = year
            last_month = month - 1

        bills = Bill.objects.filter(
            Q(Date__month=last_month) & Q(Date__year=last_year)
        )
        if not bills:
            messages.info(request, 'No reports for last month!')
            return redirect('sales-reports')

        report_for = str(last_year) + ' - ' + str(last_month)
        generated_on = datetime.now()
        generated_by = request.user.get_full_name()

        bill_id_list = []
        total_sales = 0
        bill_count = 0
        # Calculate the total sales
        for bill in bills:
            bill_id_list.append(bill.id)
            total_sales += bill.Total_amount
            bill_count += 1

        # Get the products and each of their counts in the bill id list
        products_in_bill = BillProduct.objects.values('Product')\
            .annotate(count=Sum('QTY')).filter(Bill_Number_id__in=bill_id_list)

        # Calculate the total items sold
        total_items = 0
        product_qty_arr = []
        for product in products_in_bill:
            total_items += product.get('count')
            product_qty_arr.append(product.get('count'))

        # Get the most sold item
        max_num = get_max(product_qty_arr)
        most_sold = []
        for data in products_in_bill:
            if data.get('count') == max_num:
                product = CategoryProduct.objects.get(id=data.get('Product'))
                most_sold.append(str(product.cp_name))
        # If the most sold items are greater than 2
        # if len(most_sold) > 2:
        #     most_sold.clear()
        #     most_sold.append('Have many items')

        # Arrange data for the charts
        products_in_bill = list(products_in_bill.values_list('Product', 'Price', 'count'))
        chart_data_list = []
        chart_data_list2 = []
        for data in products_in_bill:
            product = CategoryProduct.objects.get(id=data[0])
            data_array = [str(product.cp_name), data[2]]
            data_array2 = [str(product.cp_name), data[1] * data[2]]
            chart_data_list.append(data_array)
            chart_data_list2.append(data_array2)

        # Calculate average price per bill
        average_price = round(total_sales/bill_count, 2)

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred!')
        return redirect('sales-reports')

    template = 'Outlet_Sales/PDF/salesReportTemplate.html'
    context = {'ChartData': chart_data_list,
               'ChartData2': chart_data_list2,
               'ReportFor': report_for,
               'GeneratedOn': generated_on,
               'GeneratedBy': generated_by,
               'TotalSales': total_sales,
               'TotalItems': total_items,
               'MostSold': most_sold,
               'NoOfBills': bill_count,
               'AveragePrice': average_price,
               }
    return render(request, template, context)


@login_required(login_url=loginUrl)
def report_last_year(request):
    try:
        year = datetime.now().year
        last_year = year - 1

        bills = Bill.objects.filter(Q(Date__year=last_year))
        if not bills:
            messages.info(request, 'No reports for last year!')
            return redirect('sales-reports')

        report_for = last_year
        generated_on = datetime.now()
        generated_by = request.user.get_full_name()

        bill_id_list = []
        total_sales = 0
        bill_count = 0
        # Calculate the total sales
        for bill in bills:
            bill_id_list.append(bill.id)
            total_sales += bill.Total_amount
            bill_count += 1

        # Get the products and each of their counts in the bill id list
        products_in_bill = BillProduct.objects.values('Product')\
            .annotate(count=Sum('QTY')).filter(Bill_Number_id__in=bill_id_list)

        # Calculate the total items sold
        total_items = 0
        product_qty_arr = []
        for product in products_in_bill:
            total_items += product.get('count')
            product_qty_arr.append(product.get('count'))

        # Get the most sold item
        max_num = get_max(product_qty_arr)
        most_sold = []
        for data in products_in_bill:
            if data.get('count') == max_num:
                product = CategoryProduct.objects.get(id=data.get('Product'))
                most_sold.append(str(product.cp_name))
        # If the most sold items are greater than 2
        # if len(most_sold) > 2:
        #     most_sold.clear()
        #     most_sold.append('Have many items')

        # Arrange data for the charts
        products_in_bill = list(products_in_bill.values_list('Product', 'Price', 'count'))
        chart_data_list = []
        chart_data_list2 = []
        for data in products_in_bill:
            product = CategoryProduct.objects.get(id=data[0])
            data_array = [str(product.cp_name), data[2]]
            data_array2 = [str(product.cp_name), data[1] * data[2]]
            chart_data_list.append(data_array)
            chart_data_list2.append(data_array2)

        # Calculate average price per bill
        average_price = round(total_sales/bill_count, 2)

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred!')
        return redirect('sales-reports')

    template = 'Outlet_Sales/PDF/salesReportTemplate.html'
    context = {'ChartData': chart_data_list,
               'ChartData2': chart_data_list2,
               'ReportFor': report_for,
               'GeneratedOn': generated_on,
               'GeneratedBy': generated_by,
               'TotalSales': total_sales,
               'TotalItems': total_items,
               'MostSold': most_sold,
               'NoOfBills': bill_count,
               'AveragePrice': average_price,
               }
    return render(request, template, context)


@login_required(login_url=loginUrl)
def report_specific_month(request):
    if request.method == "POST":
        selected_month = request.POST.get('month')
    else:
        return redirect('sales-reports')
    try:
        bills = Bill.objects.filter(Q(Date__icontains=selected_month))
        if not bills:
            messages.info(request, 'No reports for ' + str(selected_month))
            return redirect('sales-reports')

        report_for = selected_month
        generated_on = datetime.now()
        generated_by = request.user.get_full_name()

        bill_id_list = []
        total_sales = 0
        bill_count = 0
        # Calculate the total sales
        for bill in bills:
            bill_id_list.append(bill.id)
            total_sales += bill.Total_amount
            bill_count += 1

        # Get the products and each of their counts in the bill id list
        products_in_bill = BillProduct.objects.values('Product')\
            .annotate(count=Sum('QTY')).filter(Bill_Number_id__in=bill_id_list)

        # Calculate the total items sold
        total_items = 0
        product_qty_arr = []
        for product in products_in_bill:
            total_items += product.get('count')
            product_qty_arr.append(product.get('count'))

        # Get the most sold item
        max_num = get_max(product_qty_arr)
        most_sold = []
        for data in products_in_bill:
            if data.get('count') == max_num:
                product = CategoryProduct.objects.get(id=data.get('Product'))
                most_sold.append(str(product.cp_name))
        # If the most sold items are greater than 2
        # if len(most_sold) > 2:
        #     most_sold.clear()
        #     most_sold.append('Have many items')

        # Arrange data for the charts
        products_in_bill = list(products_in_bill.values_list('Product', 'Price', 'count'))
        chart_data_list = []
        chart_data_list2 = []
        for data in products_in_bill:
            product = CategoryProduct.objects.get(id=data[0])
            data_array = [str(product.cp_name), data[2]]
            data_array2 = [str(product.cp_name), data[1] * data[2]]
            chart_data_list.append(data_array)
            chart_data_list2.append(data_array2)

        # Calculate average price per bill
        average_price = round(total_sales/bill_count, 2)

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred!')
        return redirect('sales-reports')

    template = 'Outlet_Sales/PDF/salesReportTemplate.html'
    context = {'ChartData': chart_data_list,
               'ChartData2': chart_data_list2,
               'ReportFor': report_for,
               'GeneratedOn': generated_on,
               'GeneratedBy': generated_by,
               'TotalSales': total_sales,
               'TotalItems': total_items,
               'MostSold': most_sold,
               'NoOfBills': bill_count,
               'AveragePrice': average_price,
               }
    return render(request, template, context)


@login_required(login_url=loginUrl)
def report_specific_year(request):
    if request.method == "POST":
        selected_year = request.POST.get('year')
    else:
        return redirect('sales-reports')
    try:
        bills = Bill.objects.filter(Q(Date__year=selected_year))
        if not bills:
            messages.info(request, 'No reports for '+str(selected_year))
            return redirect('sales-reports')

        report_for = selected_year
        generated_on = datetime.now()
        generated_by = request.user.get_full_name()

        bill_id_list = []
        total_sales = 0
        bill_count = 0
        # Calculate the total sales
        for bill in bills:
            bill_id_list.append(bill.id)
            total_sales += bill.Total_amount
            bill_count += 1

        # Get the products and each of their counts in the bill id list
        products_in_bill = BillProduct.objects.values('Product')\
            .annotate(count=Sum('QTY')).filter(Bill_Number_id__in=bill_id_list)

        # Calculate the total items sold
        total_items = 0
        product_qty_arr = []
        for product in products_in_bill:
            total_items += product.get('count')
            product_qty_arr.append(product.get('count'))

        # Get the most sold item
        max_num = get_max(product_qty_arr)
        most_sold = []
        for data in products_in_bill:
            if data.get('count') == max_num:
                product = CategoryProduct.objects.get(id=data.get('Product'))
                most_sold.append(str(product.cp_name))
        # If the most sold items are greater than 2
        # if len(most_sold) > 2:
        #     most_sold.clear()
        #     most_sold.append('Have many items')

        # Arrange data for the charts
        products_in_bill = list(products_in_bill.values_list('Product', 'Price', 'count'))
        chart_data_list = []
        chart_data_list2 = []
        for data in products_in_bill:
            product = CategoryProduct.objects.get(id=data[0])
            data_array = [str(product.cp_name), data[2]]
            data_array2 = [str(product.cp_name), data[1] * data[2]]
            chart_data_list.append(data_array)
            chart_data_list2.append(data_array2)

        # Calculate average price per bill
        average_price = round(total_sales/bill_count, 2)

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred!')
        return redirect('sales-reports')

    template = 'Outlet_Sales/PDF/salesReportTemplate.html'
    context = {'ChartData': chart_data_list,
               'ChartData2': chart_data_list2,
               'ReportFor': report_for,
               'GeneratedOn': generated_on,
               'GeneratedBy': generated_by,
               'TotalSales': total_sales,
               'TotalItems': total_items,
               'MostSold': most_sold,
               'NoOfBills': bill_count,
               'AveragePrice': average_price,
               }
    return render(request, template, context)
