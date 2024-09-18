from django.contrib import admin

from .models import Product
from .models import ProductDetail
from .models import Ingredient,HSNCode
from .models import ProductBatch, ProductDetailBatch
from .models import CustomerDetail
from .models import Bill, BillItems, BillItemsTest,BillTest2, BillItemsTest2
# Register your models here.
admin.site.register(Product)
# admin.site.register(ProductDetail)
admin.site.register(Ingredient)
admin.site.register(ProductBatch)
# admin.site.register(ProductDetailBatch)
admin.site.register(CustomerDetail)
# admin.site.register(Bill)
admin.site.register(BillItems)
admin.site.register(BillItemsTest)
admin.site.register(BillItemsTest2)
admin.site.register(HSNCode)

class BillItemsInline(admin.TabularInline):
    model = BillItemsTest2
    extra = 2

class BillAdmin(admin.ModelAdmin):
    fields = ['customer','purchase_date']
    inlines = [BillItemsInline]

admin.site.register(BillTest2, BillAdmin)

class ProductDetailBatchAdmin(admin.ModelAdmin):
    list_display = ('__str__','batch_no','packing', 'quantity','price')

admin.site.register(ProductDetailBatch,ProductDetailBatchAdmin)