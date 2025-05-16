from django.db.models import Sum, F, Value, DecimalField
from django.shortcuts import render, redirect
from .models import Receipt, Issued, Production_Issued, Production_Return
from .forms import Receipt_Form, Issued_Form, Production_Issued_Form, Production_Return_Form
# Create your views here.
# def home(request):
#     return render(request, 'home.html')

def receipt(request):
    datas = Receipt.objects.all()
    if request.method == 'POST':
        form = Receipt_Form(request.POST)
        if form.is_valid():
            data = form.save(commit= False)
            data.save()
            return redirect('receipt')
    else:
        form = Receipt_Form()
    return render(request, 'receipt.html', {'form':form, 'datas':datas})

def issued(request):
    datas = Issued.objects.all()
    if request.method == 'POST':
        form = Issued_Form(request.POST)
        if form.is_valid():
            data = form.save(commit= False)
            data.save()
            return redirect('issued')
    else:
        form = Issued_Form()
   
    return render(request, 'issued.html', {'form':form, 'datas':datas})

def production_issued(request):
    datas = Production_Issued.objects.all()
    if request.method == 'POST':
        form = Production_Issued_Form(request.POST)
        if form.is_valid():
            data = form.save(commit= False)
            data.save()
            return redirect('production_issued')
    else:
        form = Production_Issued_Form()
    return render(request, 'production_issued.html', {'form':form, 'datas':datas})

def production_return(request):
    datas = Production_Return.objects.all()
    if request.method == 'POST':
        form = Production_Return_Form(request.POST)
        if form.is_valid():
            data = form.save(commit= False)
            data.save()
            return redirect('production_return')
    else:
        form = Production_Return_Form()
    return render(request, 'production_return.html', {'form':form, 'datas':datas})



def home(request):
    # Grouping by common stock-identifying fields (you can customize)
    group_fields = ['yarn_count', 'content', 'yarn_lot','colour']

    # Total Received
    received = (
        Receipt.objects.values(*group_fields)
        .annotate(total=Sum('net_weight'))
    )

    # Total Issued
    issued = (
        Issued.objects.values(*group_fields)
        .annotate(total=Sum('net_weight'))
    )

    # Total Production Issued
    prod_issued = (
        Production_Issued.objects.values(*group_fields)
        .annotate(total=Sum('net_weight'))
    )

    # Total Production Return
    prod_return = (
        Production_Return.objects.values(*group_fields)
        .annotate(total=Sum('net_weight'))
    )

    # Build a stock dictionary
    stock = {}

    def add_to_stock(queryset, key, factor=1):
        for item in queryset:
            k = tuple(item[field] for field in group_fields)
            stock.setdefault(k, {'received': 0, 'issued': 0, 'prod_issued': 0, 'prod_return': 0})
            stock[k][key] += float(item['total']) * factor

    add_to_stock(received, 'received')
    add_to_stock(issued, 'issued', -1)
    add_to_stock(prod_issued, 'prod_issued', -1)
    add_to_stock(prod_return, 'prod_return')

    # Convert to list for template
    stock_list = []
    for key, value in stock.items():
        yarn_count, content, yarn_lot, colour = key
        total = sum(value.values())
        stock_list.append({
            'yarn_count': yarn_count,
            'content': content,
            'yarn_lot': yarn_lot,
            'colour':colour,
            'received': value['received'],
            'issued': -value['issued'],
            'prod_issued': -value['prod_issued'],
            'prod_return': value['prod_return'],
            'total_stock': total,
        })

    return render(request, 'home.html', {'stock_list': stock_list})

## PRODUCTION REPORT LOGIC
from django.db.models import Sum

def production_report(request):
    issued_bills = Production_Issued.objects.values_list('bill_no', flat=True).distinct()
    return_bills = Production_Return.objects.values_list('bill_no', flat=True).distinct()
    all_bills = set(issued_bills).union(set(return_bills))

    merged_data = []

    for bill in all_bills:
        issued_qs = Production_Issued.objects.filter(bill_no=bill)
        return_qs = Production_Return.objects.filter(bill_no=bill)

        issued = issued_qs.first()
        returned = return_qs.first()

        issued_weight = issued_qs.aggregate(Sum('net_weight'))['net_weight__sum'] or 0
        returned_weight = return_qs.aggregate(Sum('net_weight'))['net_weight__sum'] or 0

        merged_data.append({
            'bill_no': bill,
            'date': issued.date if issued else returned.date,
            'article': issued.article if issued else '',
            'no_of_article': issued.no_of_article if issued else '',
            'average_weight_of_article': issued.average_weight_of_article if issued else '',
            'required_weight_for_prod': issued.required_weight_for_prod if issued else '',
            'name': issued.name if issued else returned.name,
            'yarn_lot': issued.yarn_lot if issued else '',
            'content': issued.content if issued else '',
            'yarn_count': issued.yarn_count if issued else '',
            'colour': issued.colour if issued else '',
            'cone_out': issued.no_of_cones if issued else '',
            'gross_out': issued.gross_weight if issued else '',
            'net_out': issued_weight,
            'cone_in': returned.no_of_cones if returned else '',
            'gross_in': returned.gross_weight if returned else '',
            'net_in': returned_weight,
            'total_usage': issued_weight - returned_weight,
            'returned_pcs': returned.no_of_article if returned else '',
            'weight_of_pcs': returned.average_weight_of_article if returned else '',
            'yarn_wastage': returned.yarn_wastage if returned else '',
        })

    return render(request, 'production_report.html', {'merged_data': merged_data})

