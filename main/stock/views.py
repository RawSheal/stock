from django.db.models import Sum, F, Value, DecimalField
from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipt, Issued, Production_Issued, Production_Return
from .forms import Receipt_Form, Issued_Form, Production_Issued_Form, Production_Return_Form
# Create your views here.
# def home(request):
#     return render(request, 'home.html')

def receipt(request):
    datas = Receipt.objects.all().order_by('-date')

    # Filters from GET request
    bill_no = request.GET.get('bill_no')
    name = request.GET.get('name')
    content = request.GET.get('content')
    colour = request.GET.get('colour')
    yarn_count = request.GET.get('yarn_count')
    receipt_type = request.GET.get('receipt_type')

    if bill_no:
        datas = datas.filter(bill_no__icontains=bill_no)
    if name:
        datas = datas.filter(name__icontains=name)
    if content:
        datas = datas.filter(content__iexact=content)
    if yarn_count:
        datas = datas.filter(yarn_count__iexact=yarn_count)
    if colour:
        datas = datas.filter(colour__icontains=colour)
    if receipt_type:
        datas = datas.filter(receipt_type=receipt_type)

    if request.method == 'POST':
        form = Receipt_Form(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect('receipt')
    else:
        form = Receipt_Form()

    context = {
        'form': form,
        'datas': datas,
        'filters': {
            'bill_no': bill_no or '',
            'name': name or '',
            'content': content or '',
            'colour': colour or '',
            'yarn_count': yarn_count or '',
            'receipt_type': receipt_type or '',
        }
    }
    return render(request, 'receipt.html', context)


def issued(request):
    datas = Issued.objects.all().order_by('-date')
    
    # Filters from GET request
    bill_no = request.GET.get('bill_no')
    name = request.GET.get('name')
    content = request.GET.get('content')
    colour = request.GET.get('colour')
    yarn_count = request.GET.get('yarn_count')

    if bill_no:
        datas = datas.filter(bill_no__icontains=bill_no)
    if name:
        datas = datas.filter(name__icontains=name)
    if content:
        datas = datas.filter(content__iexact=content)
    if yarn_count:
        datas = datas.filter(yarn_count__iexact=yarn_count)
    if colour:
        datas = datas.filter(colour__icontains=colour)
    
    if request.method == 'POST':
        form = Issued_Form(request.POST)
        if form.is_valid():
            data = form.save(commit= False)
            data.save()
            return redirect('issued')
    else:
        form = Issued_Form()
        
    context = {
        'form': form,
        'datas': datas,
        'filters': {
            'bill_no': bill_no or '',
            'name': name or '',
            'content': content or '',
            'colour': colour or '',
            'yarn_count': yarn_count or '',
        }
    }
   
    return render(request, 'issued.html', context)

def production_issued(request):
    datas = Production_Issued.objects.all().order_by('-date')
    
     # Filters from GET request
    bill_no = request.GET.get('bill_no')
    name = request.GET.get('name')
    content = request.GET.get('content')
    colour = request.GET.get('colour')
    yarn_count = request.GET.get('yarn_count')

    if bill_no:
        datas = datas.filter(bill_no__icontains=bill_no)
    if name:
        datas = datas.filter(name__icontains=name)
    if content:
        datas = datas.filter(content__iexact=content)
    if yarn_count:
        datas = datas.filter(yarn_count__iexact=yarn_count)
    if colour:
        datas = datas.filter(colour__icontains=colour)
    
    if request.method == 'POST':
        form = Production_Issued_Form(request.POST)
        if form.is_valid():
            data = form.save(commit= False)
            data.save()
            return redirect('production_issued')
    else:
        form = Production_Issued_Form()
    context = {
        'form': form,
        'datas': datas,
        'filters': {
            'bill_no': bill_no or '',
            'name': name or '',
            'content': content or '',
            'colour': colour or '',
            'yarn_count': yarn_count or '',
        }
    }
    return render(request, 'production_issued.html', context)

def production_return(request):
    datas = Production_Return.objects.all().order_by('-date')
    
     # Filters from GET request
    bill_no = request.GET.get('bill_no')
    name = request.GET.get('name')
    content = request.GET.get('content')
    colour = request.GET.get('colour')
    yarn_count = request.GET.get('yarn_count')

    if bill_no:
        datas = datas.filter(bill_no__icontains=bill_no)
    if name:
        datas = datas.filter(name__icontains=name)
    if content:
        datas = datas.filter(content__iexact=content)
    if yarn_count:
        datas = datas.filter(yarn_count__iexact=yarn_count)
    if colour:
        datas = datas.filter(colour__icontains=colour)
    
    if request.method == 'POST':
        form = Production_Return_Form(request.POST)
        if form.is_valid():
            data = form.save(commit= False)
            data.save()
            return redirect('production_return')
    else:
        form = Production_Return_Form()
        
    context = {
        'form': form,
        'datas': datas,
        'filters': {
            'bill_no': bill_no or '',
            'name': name or '',
            'content': content or '',
            'colour': colour or '',
            'yarn_count': yarn_count or '',
        }
    }
    return render(request, 'production_return.html', context)




def home(request):
    group_fields = ['yarn_count', 'content', 'yarn_lot', 'colour']

    # Filters from GET
    filters = {
        'yarn_lot': request.GET.get('yarn_lot', ''),
        'content': request.GET.get('content', ''),
        'colour': request.GET.get('colour', ''),
        'yarn_count': request.GET.get('yarn_count', ''),
        'status': request.GET.get('status', ''),
    }

    # Base querysets
    receipt_qs = Receipt.objects.all().order_by('-date')
    issued_qs = Issued.objects.all().order_by('-date')
    prod_issued_qs = Production_Issued.objects.all().order_by('-date')
    prod_return_qs = Production_Return.objects.all().order_by('-date')

    # Apply filters (excluding 'status')
    for field, value in filters.items():
        if field == 'status':
            continue
        if value:
            kwargs_icontains = {f"{field}__icontains": value}
            receipt_qs = receipt_qs.filter(**kwargs_icontains)
            issued_qs = issued_qs.filter(**kwargs_icontains)
            prod_issued_qs = prod_issued_qs.filter(**kwargs_icontains)
            prod_return_qs = prod_return_qs.filter(**kwargs_icontains)

    # Grouped aggregation
    received = receipt_qs.values(*group_fields).annotate(total=Sum('net_weight'))
    issued = issued_qs.values(*group_fields).annotate(total=Sum('net_weight'))
    prod_issued = prod_issued_qs.values(*group_fields).annotate(total=Sum('net_weight'))
    prod_return = prod_return_qs.values(*group_fields).annotate(total=Sum('net_weight'))

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

    stock_list = []
    for key, value in stock.items():
        yarn_count, content, yarn_lot, colour = key
        total = sum(value.values())

        # Filter based on stock status
        if filters['status'] == 'in_stock' and total <= 0:
            continue
        if filters['status'] == 'out_of_stock' and total > 0:
            continue

        stock_list.append({
            'yarn_count': yarn_count,
            'content': content,
            'yarn_lot': yarn_lot,
            'colour': colour,
            'received': value['received'],
            'issued': -value['issued'],
            'prod_issued': -value['prod_issued'],
            'prod_return': value['prod_return'],
            'total_stock': total,
        })

    return render(request, 'home.html', {'stock_list': stock_list, 'filters': filters})


## PRODUCTION REPORT LOGIC
from django.db.models import Sum

def production_report(request):
    filters = {
        'bill_no': request.GET.get('bill_no', ''),
        'name': request.GET.get('name', ''),
        'content': request.GET.get('content', ''),
        'colour': request.GET.get('colour', ''),
        'yarn_count': request.GET.get('yarn_count', ''),
        'status': request.GET.get('status', ''),
    }

    # Apply field-based filters to issued and returned querysets
    issued_qs = Production_Issued.objects.all()
    return_qs = Production_Return.objects.all()

    for field, value in filters.items():
        if value and field != 'status':  # Don't apply 'status' to ORM filters
            kwargs_icontains = {f"{field}__icontains": value}
            issued_qs = issued_qs.filter(**kwargs_icontains)
            return_qs = return_qs.filter(**kwargs_icontains)

    issued_bills = issued_qs.values_list('bill_no', flat=True).distinct()
    return_bills = return_qs.values_list('bill_no', flat=True).distinct()
    all_bills = set(issued_bills).union(set(return_bills))

    merged_data = []

    for bill in all_bills:
        issued = issued_qs.filter(bill_no=bill)
        returned = return_qs.filter(bill_no=bill)

        i = issued.first()
        r = returned.first()

        issued_weight = issued.aggregate(Sum('net_weight'))['net_weight__sum'] or 0
        returned_weight = returned.aggregate(Sum('net_weight'))['net_weight__sum'] or 0

        gross_in = r.gross_weight if r else ''

        data = {
            'bill_no': bill,
            'date': i.date if i else r.date,
            'article': i.article if i else '',
            'no_of_article': i.no_of_article if i else '',
            'average_weight_of_article': i.average_weight_of_article if i else '',
            'required_weight_for_prod': i.required_weight_for_prod if i else '',
            'name': i.name if i else r.name,
            'yarn_lot': i.yarn_lot if i else '',
            'content': i.content if i else '',
            'yarn_count': i.yarn_count if i else '',
            'colour': i.colour if i else '',
            'cone_out': i.no_of_cones if i else '',
            'gross_out': i.gross_weight if i else '',
            'net_out': issued_weight,
            'cone_in': r.no_of_cones if r else '',
            'gross_in': gross_in,
            'net_in': returned_weight,
            'total_usage': issued_weight - returned_weight,
            'returned_pcs': r.no_of_article if r else '',
            'weight_of_pcs': r.average_weight_of_article if r else '',
            'yarn_wastage': r.yarn_wastage if r else '',
        }

        merged_data.append(data)

    # ✅ Apply status filter after building the list
    status_filter = filters['status']
    if status_filter == 'pending':
        merged_data = [item for item in merged_data if not item['gross_in']]
    elif status_filter == 'done':
        merged_data = [item for item in merged_data if item['gross_in']]

    return render(request, 'production_report.html', {
        'merged_data': merged_data,
        'filters': filters
    })



def receipt_edit(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    
    if request.method == 'POST':
        form = Receipt_Form(request.POST, instance=receipt)
        if form.is_valid():
            form.save()
            return redirect('receipt')
    else:
        form = Receipt_Form(instance=receipt)
    
    return render(request, 'edit_page/receipt_edit.html', {'receipt':receipt, 'form':form})


def issued_edit(request, pk):
    issued = get_object_or_404(Issued, pk=pk)
    
    if request.method == 'POST':
        form = Issued_Form(request.POST, instance=issued)
        if form.is_valid():
            form.save()
            return redirect('issued')
    else:
        form = Issued_Form(instance=issued)
    
    return render(request, 'edit_page/issued_edit.html', {'issued':issued, 'form':form})


def production_issued_edit(request, pk):
    production_issued = get_object_or_404(Production_Issued, pk=pk)
    
    if request.method == 'POST':
        form = Production_Issued_Form(request.POST, instance=production_issued)
        if form.is_valid():
            form.save()
            return redirect('production_issued')
    else:
        form = Production_Issued_Form(instance=production_issued)
    
    return render(request, 'edit_page/production_issued_edit.html', {'production_issued':production_issued, 'form':form})



def production_return_edit(request, pk):
    production_return = get_object_or_404(Production_Return, pk=pk)
    
    if request.method == 'POST':
        form = Production_Return_Form(request.POST, instance=production_return)
        if form.is_valid():
            form.save()
            return redirect('production_return')
    else:
        form = Production_Return_Form(instance=production_return)
    
    return render(request, 'edit_page/production_return_edit.html', {'production_return':production_return, 'form':form})