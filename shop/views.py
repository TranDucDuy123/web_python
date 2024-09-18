from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from .models import Product,ProductDetailBatch,CustomerDetail,Bill,BillItems,BillItemsTest, BillTest2, BillItemsTest2,Ingredient, ProductBatch,HSNCode
from .forms import BillForm,BillItemsForm,BillItemsFormset,BillItemsFormsetTest, CustomerDetailForm,ProductDetailBatchForm, IngredientForm, ProductForm, ProductBatchForm,HSNCodeForm
from django.conf import settings


def index(request):
    products_list = ProductDetailBatch.objects.all()
    customers_list = CustomerDetail.objects.all()
    bills_list = BillTest2.objects.select_related().all()
    bill_items = BillItemsTest2.objects.select_related().all()
    context = {'products_list': products_list, 'customers_list': customers_list, 'bills_list': bills_list, 'bill_items': bill_items}
    return render(request, 'shop/index.html', context)


# from django.forms.formsets import formset_factory

def add_bill(request):
    # BillItemsFormSet = formset_factory(BillItemsForm, extra=1, min_num=1, validate_min=True)
    customers_list = CustomerDetail.objects.all()
    if request.method == 'POST':
        form = BillForm(request.POST)
        formset = BillItemsFormset(request.POST)
        if all([form.is_valid(), formset.is_valid()]):
            bill = form.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    billitems = inline_form.save(commit=False)
                    billitems.purchaseno = bill
                    billitems.save()
            return redirect('shop:index')
        else:
            print('form is not valid',form,formset)
    else:
        form = BillForm(request.GET or None)
        formset = BillItemsFormset(queryset=BillItems.objects.none())

    return render(request, 'shop/add_bill.html', {'form': form,
                                                   'formset': formset, 'customers': customers_list})

def add_billtest(request):
    # BillItemsFormSet = formset_factory(BillItemsForm, extra=1, min_num=1, validate_min=True)
    customers_list = CustomerDetail.objects.all()
    if request.method == 'POST':
        form = BillForm(request.POST)
        formset = BillItemsFormsetTest(request.POST)
        if all([form.is_valid(), formset.is_valid()]):
            bill = form.save()
            products_list = ProductDetailBatch.objects.all()
            purchase_no = -1
            for inline_form in formset:
                if inline_form.cleaned_data:
                    billitems = inline_form.save(commit=False)
                    billitems.purchaseno = bill
                    purchase_no = billitems.purchaseno.purchaseno
                    isFound = False
                    pro_pk = 0
                    print('purchaseno:',billitems.purchaseno,'billitems:',billitems.productName, 'productList:', products_list)
                    for pro in products_list:
                        if pro == billitems.productName and pro.quantity >= billitems.productQuantity:
                            isFound = True
                            pro_pk = pro.pk
                            print('isFound:True', 'pro_pk:', pro_pk)
                            billitems.productBatch = pro.batch_no.batch_no
                            billitems.productPacking = pro.packing
                            billitems.productPrice = pro.price
                            billitems.productTotalPrice = float(pro.price) * int(billitems.productQuantity)
                            break
                    if isFound:
                        productObj = ProductDetailBatch.objects.get(pk = pro_pk)
                        productObj.quantity -= billitems.productQuantity
                        print('productObj:', productObj, productObj.quantity)
                        billitems.save()
                        productObj.save()
                    else:
                        billObj = BillTest2.objects.get(purchaseno=bill.purchaseno)
                        billObj.delete()
                        return redirect('shop:product_packing')
            return redirect('shop:show', purchase_no)
        else:
            print('form is not valid',form,formset)
    else:
        form = BillForm(request.GET or None)
        formset = BillItemsFormsetTest(queryset=BillItems.objects.none())

    return render(request, 'shop/add_bill.html', {'form': form,
                                                   'formset': formset, 'customers': customers_list})


def show(request,purchaseno):
    bills_list = BillTest2.objects.select_related().all().filter(purchaseno=purchaseno)
    bill_items = BillItemsTest2.objects.select_related().all().filter(purchaseno=purchaseno)
    totalamount = 0
    totalamount_without_tax = 0
    total_tax = 0
    from .templatetags.calculate_tax import without_tax, tax
    for item in bill_items:
        totalamount += item.productTotalPrice
        totalamount_without_tax += without_tax(item.productTotalPrice, item.productName.batch_no.product.hsn_code.rate)
        total_tax += tax(item.productTotalPrice, item.productName.batch_no.product.hsn_code.rate)

    context = {'bills_list': bills_list, 'bill_items': bill_items, 'totalamount': totalamount, 'totalamount_without_tax': totalamount_without_tax, 'total_tax': total_tax}
    return render(request, 'shop/show.html', context)

def edit_billtest(request, purchaseno,customer_id):
    # BillItemsFormSet = formset_factory(BillItemsForm, extra=1, min_num=1, validate_min=True)
    bills = BillTest2.objects.get(purchaseno=purchaseno)
    bill_items = BillItemsTest2.objects.select_related().all().filter(purchaseno=purchaseno)
    customers_list = CustomerDetail.objects.all()
    if request.method == 'POST':
        form = BillForm(request.POST, instance = bills)
        formset = BillItemsFormsetTest(request.POST, queryset=bill_items)
        if all([form.is_valid(), formset.is_valid()]):
            bill = form.save()
            products_list = ProductDetailBatch.objects.all()
            purchase_no = -1
            for inline_form in formset:
                if inline_form.cleaned_data:
                    billitems = inline_form.save(commit=False)
                    billitems.purchaseno = bill
                    purchase_no = billitems.purchaseno.purchaseno
                    print('purchaseno:',billitems.purchaseno,'billitems:',billitems.productName, 'productList:', products_list)
                    for pro in products_list:
                        if pro == billitems.productName:
                            billitems.productBatch = pro.batch_no.batch_no
                            billitems.productPacking = pro.packing
                            billitems.productPrice = pro.price
                            billitems.productTotalPrice = float(pro.price) * int(billitems.productQuantity)
                            break
                    billitems.save()
            return redirect('shop:show', purchase_no)
        else:
            print('form is not valid',form.errors,formset.errors)
    else:
        form = BillForm(instance = bills)
        formset = BillItemsFormsetTest(queryset=bill_items)

    return render(request, 'shop/edit_bill.html', {'form': form,
                                                   'formset': formset, 'customers': customers_list})

def dashboard(request):
    total_product = Product.objects.count()
    total_buyer = CustomerDetail.objects.count()
    total_order = BillTest2.objects.count()
    orders = BillTest2.objects.select_related().all().order_by('-purchaseno')
    from datetime import date
    expired = ProductBatch.objects.all().filter(expirydate__lte = date.today()).count()
    context = {
        'product': total_product,
        'buyer': total_buyer,
        'order': total_order,
        'orders': orders,
        'expired': expired,
        'site-url': settings.SITE_URL
    }
    return render(request, 'shop/dashboard.html', context)

def add_customer(request):
    if request.method == 'POST':
        form = CustomerDetailForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect('shop:dashboard')
        else:
            print('form is not valid',form)
    else:
        form = CustomerDetailForm(request.GET or None)
    return render(request, 'shop/add_customer.html', {'form': form, 'btn_add_edit': 'Create'})

def customers(request):
    customers_list = CustomerDetail.objects.all()
    context = {'customers_list': customers_list}
    return render(request, 'shop/view_customer.html', context)

def edit_customer(request, pk):
    customer = CustomerDetail.objects.get(pk=pk)
    if request.method == 'POST':
        form = CustomerDetailForm(request.POST,instance = customer)
        if form.is_valid():
            customer = form.save()
            return redirect('shop:customers')
        else:
            print('form is not valid',form)
    else:
        form = CustomerDetailForm(instance = customer)
    return render(request, 'shop/add_customer.html', {'form': form, 'btn_add_edit': 'Update'})

def product_packing(request):
    products_list = ProductDetailBatch.objects.all()
    context = {'products_list': products_list}
    return render(request, 'shop/view_products_packing.html', context)

def add_product_packing(request):
    if request.method == 'POST':
        form = ProductDetailBatchForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('shop:product_packing')
        else:
            print('form is not valid',form)
    else:
        form = ProductDetailBatchForm(request.GET or None)
    return render(request, 'shop/add_product_packing.html', {'form': form, 'btn_add_edit': 'Create'})

def edit_product_packing(request, pk):
    productbatch = ProductDetailBatch.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductDetailBatchForm(request.POST,instance = productbatch)
        if form.is_valid():
            productbatch = form.save()
            return redirect('shop:product_packing')
        else:
            print('form is not valid',form)
    else:
        form = ProductDetailBatchForm(instance = productbatch)
    return render(request, 'shop/add_product_packing.html', {'form': form, 'btn_add_edit': 'Update'})

def add_product_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('shop:add_product')
        else:
            print('form is not valid',form)
    else:
        form = IngredientForm(request.GET or None)
    return render(request, 'shop/add_product_ingredient.html', {'form': form, 'btn_add_edit': 'Create'})

def product_ingredient(request):
    ingredients_list = Ingredient.objects.all()
    context = {'ingredients_list': ingredients_list}
    return render(request, 'shop/view_product_ingredients.html', context)

def edit_ingredient(request, pk):
    ingredient = Ingredient.objects.get(pk=pk)
    if request.method == 'POST':
        form = IngredientForm(request.POST,instance = ingredient)
        if form.is_valid():
            ingredient = form.save()
            return redirect('shop:product_ingredient')
        else:
            print('form is not valid',form)
    else:
        form = IngredientForm(instance = ingredient)
    return render(request, 'shop/add_product_ingredient.html', {'form': form, 'btn_add_edit': 'Update'})

def product(request):
    products_list = Product.objects.all()
    context = {'products_list': products_list}
    return render(request, 'shop/view_products.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print('POST data:', request.POST)
        print('FILES data:', request.FILES)  # Kiểm tra xem file có đến không
        
        if form.is_valid():
            product = form.save()
            print('Product saved:', product)
            print('File uploaded:', request.FILES)  # Kiểm tra file đã được upload chưa
            return redirect('shop:add_product_batch')
        else:
            print('Form is not valid:', form.errors)
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form, 'btn_add_edit': 'Create'})

def edit_product(request,pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,instance = product)
        if form.is_valid():
            product = form.save()
            return redirect('shop:product')
        else:
            print('form is not valid',form)
    else:
        form = ProductForm(instance = product)
    return render(request, 'shop/add_product.html', {'form': form, 'btn_add_edit': 'Update'})

def product_batch(request):
    products_list = ProductBatch.objects.all()
    from datetime import date, timedelta
    today = date.today()
    today30 = date.today() + timedelta(30)
    context = {
        'today': today,
        'today30': today30,
        'products_list': products_list
    }
    return render(request, 'shop/view_products_batch.html', context)

def add_product_batch(request):
    if request.method == 'POST':
        form = ProductBatchForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('shop:add_product_packing')
        else:
            print('form is not valid',form)
    else:
        form = ProductBatchForm(request.GET or None)
    return render(request, 'shop/add_product_batch.html', {'form': form, 'btn_add_edit': 'Create'})

def edit_product_batch(request,pk):
    product = ProductBatch.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductBatchForm(request.POST, instance = product)
        if form.is_valid():
            product = form.save()
            return redirect('shop:product_batch')
        else:
            print('form is not valid',form)
    else:
        form = ProductBatchForm(instance = product)
    return render(request, 'shop/add_product_batch.html', {'form': form, 'btn_add_edit': 'Update'})

def delete_ingredient(request, pk):
    obj = Ingredient.objects.get(pk=pk)
    obj.delete()
    return redirect('shop:product_ingredient')

def delete_customers(request, pk):
    obj = CustomerDetail.objects.get(pk=pk)
    obj.delete()
    return redirect('shop:customers')

def delete_product_batch(request, pk):
    obj = ProductBatch.objects.get(pk=pk)
    obj.delete()
    return redirect('shop:product_batch')

def delete_product_packing(request, pk):
    obj = ProductDetailBatch.objects.get(pk=pk)
    obj.delete()
    return redirect('shop:product_packing')

def delete_product(request, pk):
    obj = Product.objects.get(pk=pk)
    obj.delete()
    return redirect('shop:product')

def delete_order(request, pk):
    obj = BillTest2.objects.get(pk=pk)
    obj.delete()
    return redirect('shop:dashboard')

def expired_product(request):
    from datetime import date, timedelta
    expired = ProductBatch.objects.all().filter(expirydate__lte = date.today()+ timedelta(30))
    today = date.today()
    today30 = date.today() + timedelta(30)
    context = {
        'expired': expired,
        'today': today,
        'today30': today30
    }
    return render(request, 'shop/view_expired_products.html', context)

def edit_billtest_final(request, purchaseno,customer_id):
    # BillItemsFormSet = formset_factory(BillItemsForm, extra=1, min_num=1, validate_min=True)
    bills = BillTest2.objects.get(purchaseno=purchaseno)
    bill_items = BillItemsTest2.objects.select_related().all().filter(purchaseno=purchaseno)
    customers_list = CustomerDetail.objects.all()
    if request.method == 'POST':
        form = BillForm(request.POST, instance = bills)
        formset = BillItemsFormsetTest(request.POST, queryset=bill_items)
        if all([form.is_valid(), formset.is_valid()]):
            bill = form.save()
            products_list = ProductDetailBatch.objects.all()
            purchase_no = -1
            for inline_form in formset:
                if inline_form.cleaned_data:
                    billitems = inline_form.save(commit=False)
                    billitems.purchaseno = bill
                    purchase_no = billitems.purchaseno.purchaseno
                    isFound =False
                    pro_pk = 0
                    print('purchaseno:',billitems.purchaseno,'billitems:',billitems.productName, 'productList:', products_list)
                    for pro in products_list:
                        if pro == billitems.productName and pro.quantity >= billitems.productQuantity:
                            isFound = True
                            pro_pk = pro.pk
                            print('isFound:True', 'pro_pk:', pro_pk)
                            billitems.productBatch = pro.batch_no.batch_no
                            billitems.productPacking = pro.packing
                            billitems.productPrice = pro.price
                            billitems.productTotalPrice = float(pro.price) * int(billitems.productQuantity)
                            break
                    if isFound:
                        productObj = ProductDetailBatch.objects.get(pk=pro_pk)
                        productObj.quantity -= billitems.productQuantity
                        print('productObj:', productObj, productObj.quantity)
                        billitems.save()
                        productObj.save()

            return redirect('shop:show', purchase_no)
        else:
            print('form is not valid',form.errors,formset.errors)
    else:
        form = BillForm(instance = bills)
        formset = BillItemsFormsetTest(queryset=bill_items)

    return render(request, 'shop/edit_bill.html', {'form': form,
                                                   'formset': formset, 'customers': customers_list})

def add_product_hsn_code(request):
    if request.method == 'POST':
        form = HSNCodeForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('shop:add_product')
        else:
            print('form is not valid',form)
    else:
        form = HSNCodeForm(request.GET or None)
    return render(request, 'shop/add_product_hsn_code.html', {'form': form, 'btn_add_edit': 'Create'})

def product_hsn_code(request):
    hsn_code_list = HSNCode.objects.all()
    context = {'hsn_code_list': hsn_code_list}
    return render(request, 'shop/view_product_hsn_code.html', context)

def edit_hsn_code(request, pk):
    hsn_code = HSNCode.objects.get(pk=pk)
    if request.method == 'POST':
        form = HSNCodeForm(request.POST,instance = hsn_code)
        if form.is_valid():
            hsn_code = form.save()
            return redirect('shop:product_hsn_code')
        else:
            print('form is not valid',form)
    else:
        form = HSNCodeForm(instance = hsn_code)
    return render(request, 'shop/add_product_hsn_code.html', {'form': form, 'btn_add_edit': 'Update'})

def delete_hsn_code(request, pk):
    obj = HSNCode.objects.get(pk=pk)
    obj.delete()
    return redirect('shop:product_hsn_code')

# def product_detail_view(request,product_id):
#     product = ProductBatch.objects.select_related().all().filter(product_id=product_id)
#     batch_list = [batch.id for batch in product]
#     productName = Product.objects.all().filter(id=product_id).distinct()
#     products_list = ProductDetailBatch.objects.select_related().all().filter(batch_no__in=batch_list)
#     context = {'products_list': products_list,'productName': productName}
#     return render(request, 'shop/view_products_detail.html', context)
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_batches = ProductBatch.objects.filter(product=product)
    product_details = ProductDetailBatch.objects.filter(batch_no__in=product_batches)

    context = {
        'product': product,
        'product_batches': product_batches,
        'product_details': product_details,
    }

    return render(request, 'shop/view_products_detail.html', context)


# scan QRcode
from django.shortcuts import render

def scan_qr_view(request):
    return render(request, 'shop/scan_qr.html')

from django.shortcuts import render, get_object_or_404
from .models import Product, ProductBatch, ProductDetailBatch

def product_summary_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_batches = ProductBatch.objects.filter(product=product)
    product_details = ProductDetailBatch.objects.filter(batch_no__in=product_batches)
    
    context = {
        'product': product,
        'product_batches': product_batches,
        'product_details': product_details,
    }
    
    return render(request, 'shop/product_summary.html', context)
