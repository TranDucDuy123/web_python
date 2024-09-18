from django import forms
from django.forms import (formset_factory, modelformset_factory)

from .models import Bill, BillItems, CustomerDetail,ProductBatch, ProductDetailBatch, BillItemsTest, BillTest2, BillItemsTest2, Ingredient,Product,HSNCode
from datetime import datetime


class BillForm(forms.ModelForm):
    
    class Meta:
        model = BillTest2
        customers_list = CustomerDetail.objects.all().values_list('name')
        fields = ('purchaseno', 'customer','purchase_date', )
        labels = {
            'purchaseno': 'Purchase No','customer': 'Customer Name','purchase_date': 'Purchase Date'
        }
        widgets = {
            'purchaseno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Purchase No here'
                }
            ),
            'customer': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Customer Name here'
                },
                choices = customers_list
            ),
            'purchase_date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Purchase Date here (YYYY-MM-DD)',
                'type':'date'
                }
            )
        }

class BillItemsForm(forms.ModelForm):
    class Meta:
        model = BillItems
        products_list = ProductDetailBatch.objects.all()
        fields = ('productName','productBatch','productPacking','productQuantity','productPrice','productTotalPrice',)
        labels = {
            'productName': 'Product Name','productBatch': 'Batch','productPacking': 'Packing','productQuantity': 'Quantity','productPrice': 'Price','productTotalPrice': 'Total Price'
        }
        widgets = {
            'productName': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Product Name here'
                },
                choices = products_list
            ),
            'productBatch': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Batch here'
                }
            ),
            'productPacking': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Packing here'
                }
            ),
            'productQuantity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Quantity here'
                }
            ),
            'productPrice': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Price here'
                }
            ),
            'productTotalPrice': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Total Price here'
                }
            )
        }

BillItemsFormset = modelformset_factory(
    BillItems,
    extra = 1,
    fields = ('productName','productBatch','productPacking','productQuantity','productPrice','productTotalPrice',),
    labels = {
        'productName': 'Product Name','productBatch': 'Batch','productPacking': 'Packing','productQuantity': 'Quantity','productPrice': 'Price','productTotalPrice': 'Total Price'
    },
    widgets = {
        'productName': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Product Name here'
            }
        ),
        'productBatch': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Batch here'
            }
        ),
        'productPacking': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Packing here'
            }
        ),
        'productQuantity': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Quantity here'
            }
        ),
        'productPrice': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Price here'
            }
        ),
        'productTotalPrice': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Total Price here'
            }
        )
    }
)
products_list = ProductDetailBatch.objects.all()
BillItemsFormsetTest = modelformset_factory(
    BillItemsTest2,
    extra = 1,
    fields = ('productName','productQuantity',),
    labels = {
        'productName': 'Product Name','productQuantity': 'Quantity'
    },
    widgets = {
        'productName': forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Product Name here'
            },
            choices = ProductDetailBatch.objects.all().values_list('batch_no')
        ),
        'productQuantity': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Quantity here'
            }
        )
    }
)



class CustomerDetailForm(forms.ModelForm):
    
    class Meta:
        model = CustomerDetail
        fields = ('name', 'address','mobile_no', )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Customer Name here'
                }
            ),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address here'
                }
            ),
            'mobile_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Mobile Number here'
                }
            )
        }

class ProductDetailBatchForm(forms.ModelForm):
    
    class Meta:
        model = ProductDetailBatch
        productbatch_list = ProductBatch.objects.all()
        fields = ('batch_no', 'packing','quantity','price', )
        widgets = {
            'batch_no': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Batch No here'
                },
                choices = productbatch_list
            ),
            'packing': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Packing here'
                }
            ),
            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Quantity here'
                }
            ),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Price here'
                }
            )
        }

class IngredientForm(forms.ModelForm):
    
    class Meta:
        model = Ingredient
        fields = ('ingredient', )
        widgets = {
            'ingredient': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Ingredient here'
                }
            )
        }

class HSNCodeForm(forms.ModelForm):
    
    class Meta:
        model = HSNCode
        fields = ('hsn_code','rate', )
        widgets = {
            'hsn_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter HSN Code here'
                }
            ),
            'rate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Rate here (in %)'
                }
            )
        }

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        ingredient = Ingredient.objects.all()
        fields = ('company','product','ingredient','hsn_code','product_image' )
        widgets = {
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Company here'
                }
            ),
            'product': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Product Name here'
                }
            ),
            'ingredient': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Ingredient here'
                },
                choices = ingredient
            ),
            'hsn_code': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter HSN Code here'
                },
                choices = ingredient
            ),
            'product_image': forms.FileInput(attrs={  # Widget để chọn file
                'class': 'form-control-file',
                'placeholder': 'Upload Product Image here'
                }
            ),

        }

class ProductBatchForm(forms.ModelForm):
    
    class Meta:
        model = ProductBatch
        product = Product.objects.all()
        fields = ('product','batch_no','mfgdate','expirydate', )
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Product Name here'
                },
                choices = product
            ),
            'batch_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Batch Number here'
                }
            ),
            'mfgdate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Manufacturing Date (YYYY-MM-DD)',
                'type':'date'
                }
            ),
            'expirydate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Expiry Date (YYYY-MM-DD)',
                'type':'date'
                }
            )

        }