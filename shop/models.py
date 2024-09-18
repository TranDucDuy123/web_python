from django.db import models
# Create your models here.
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.conf import settings
from django.urls import reverse  # Import hàm reverse để tạo URL động
import os
# Định nghĩa URL gốc của website, bạn có thể thay thế bằng domain thực tế


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=300)

    def __str__(self):
        return self.ingredient

class HSNCode(models.Model):
    hsn_code = models.CharField(max_length=50)
    rate = models.FloatField(default=18.0)

    def __str__(self):
        return "{}_ ({} %)".format(self.hsn_code,self.rate)
    
class Product(models.Model):
    company = models.CharField(max_length=100, default='None')
    product = models.CharField(max_length=100)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredients', default='None')
    hsn_code = models.ForeignKey(HSNCode, on_delete=models.CASCADE, related_name='ingredients', default='None')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    qr_code2 = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.product

    def save(self, *args, **kwargs):
        # Only generate QR codes if the object is being created
        is_new = self.pk is None
        super(Product, self).save(*args, **kwargs)  # Save to get the ID
        
        if is_new:
            self.generate_qr_codes()  # Generate QR codes after saving
            super(Product, self).save(update_fields=['qr_code', 'qr_code2'])

    def generate_qr_codes(self):
        # Generate URL for product detail view
        summary_url = settings.SITE_URL + reverse('shop:product_detail_view', args=[self.id])
        # Generate URL for product summary view
        edit_url = settings.SITE_URL + reverse('shop:product_summary_view', args=[self.id])

        # Create the first QR code
        qr1 = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr1.add_data(summary_url)
        qr1.make(fit=True)

        img1 = qr1.make_image(fill='black', back_color='white')
        buffer1 = BytesIO()
        img1.save(buffer1, format='PNG')
        filename1 = f'qr_{self.product}_detail.png'
        filebuffer1 = File(buffer1, name=filename1)
        self.qr_code.save(filename1, filebuffer1, save=False)

        # Create the second QR code
        qr2 = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr2.add_data(edit_url)
        qr2.make(fit=True)

        img2 = qr2.make_image(fill='black', back_color='white')
        buffer2 = BytesIO()
        img2.save(buffer2, format='PNG')
        filename2 = f'qr_{self.product}_summary.png'
        filebuffer2 = File(buffer2, name=filename2)
        self.qr_code2.save(filename2, filebuffer2, save=False)

    def delete(self, *args, **kwargs):
        # Delete QR code files if they exist
        if self.qr_code and os.path.isfile(self.qr_code.path):
            os.remove(self.qr_code.path)
        if self.qr_code2 and os.path.isfile(self.qr_code2.path):
            os.remove(self.qr_code2.path)
        if self.product_image and os.path.isfile(self.product_image.path):
            os.remove(self.product_image.path)
        super(Product, self).delete(*args, **kwargs)
# class Product(models.Model):
    # company = models.CharField(max_length=100, default='None')
    # product = models.CharField(max_length=100)
    # ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredients', default='None')
    # hsn_code = models.ForeignKey(HSNCode, on_delete=models.CASCADE, related_name='ingredients', default='None')
    # qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    # qr_code2 = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    # product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Thêm trường ảnh sản phẩm

    # def __str__(self):
    #     return self.product

    # def save(self, *args, **kwargs):
    #     super(Product, self).save(*args, **kwargs)
    #     if not self.qr_code:
    #         self.generate_qr_code()
    #     super(Product, self).save(*args, **kwargs)

    # def generate_qr_code(self):
    #     # Generate URL for product detail view
    #     summary_url = settings.SITE_URL + reverse('shop:product_detail_view', args=[self.id])
    #     # Generate URL for product summary view
    #     edit_url = settings.SITE_URL + reverse('shop:product_summary_view', args=[self.id])

    #     # Create the first QR code
    #     qr1 = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=4,
    #     )
    #     qr1.add_data(summary_url)
    #     qr1.make(fit=True)

    #     img1 = qr1.make_image(fill='black', back_color='white')
    #     buffer1 = BytesIO()
    #     img1.save(buffer1, format='PNG')
    #     filename1 = f'qr_{self.product}_detail.png'
    #     filebuffer1 = File(buffer1, name=filename1)
    #     self.qr_code.save(filename1, filebuffer1, save=False)

    #     # Create the second QR code
    #     qr2 = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=4,
    #     )
    #     qr2.add_data(edit_url)
    #     qr2.make(fit=True)

    #     img2 = qr2.make_image(fill='black', back_color='white')
    #     buffer2 = BytesIO()
    #     img2.save(buffer2, format='PNG')
    #     filename2 = f'qr_{self.product}_summary.png'
    #     filebuffer2 = File(buffer2, name=filename2)
    #     self.qr_code2.save(filename2, filebuffer2, save=False)

    # def delete(self, *args, **kwargs):
    #     # Xóa file QR code nếu nó tồn tại
    #     if self.qr_code:
    #         if os.path.isfile(self.qr_code.path):
    #             os.remove(self.qr_code.path)
    #     # Xóa hình ảnh sản phẩm nếu tồn tại
    #     if self.product_image:
    #         if os.path.isfile(self.product_image.path):
    #             os.remove(self.product_image.path)
    #     # Gọi phương thức delete() mặc định để xóa sản phẩm
    #     super(Product, self).delete(*args, **kwargs)

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=50)
    mfgdate = models.DateTimeField('manufacture')
    expirydate = models.DateTimeField('expiry date')
    packing = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return "{}_{}_{}".format(self.product.product, self.batch_no, self.packing)

class ProductBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=50, default='')
    mfgdate = models.DateField('manufacture')
    expirydate = models.DateField('expiry date')
    # packing = models.CharField(max_length=50)
    # quantity = models.IntegerField(default=0)
    # price = models.FloatField(default=0)

    def __str__(self):
        return "{}_{}".format(self.product.product, self.batch_no)

class ProductDetailBatch(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch_no = models.ForeignKey(ProductBatch, on_delete=models.CASCADE) #models.CharField(max_length=50)
    packing = models.CharField(max_length=50, default='')
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return "{}_{}_{}".format(self.batch_no.product.product,self.batch_no.batch_no, self.packing)

class CustomerDetail(models.Model):
    name = models.CharField(max_length=100)
    joining_date = models.DateField('joining date', auto_now_add=True)
    address = models.CharField(max_length=150,blank=True)
    mobile_no = models.BigIntegerField(blank=True,null=True)

    def __str__(self):
        if self.mobile_no:
            return "{} {}".format(self.name, self.mobile_no)
        else:
            return "{}".format(self.name)

class Bill(models.Model):
    purchaseno = models.IntegerField(default=1)
    customer = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE)
    purchase_date = models.DateField('purchase date')

    def __str__(self):
        return "{}_{}".format(self.customer.name,self.purchaseno)

class BillItems(models.Model):
    purchaseno = models.ForeignKey(Bill, related_name="bills", on_delete=models.CASCADE)
    # productName = self.product.batch_no.product.product
    # productBatch = self.product.batch_no.batch_no
    # productPacking = self.product.packing
    # productQuantity = models.IntegerField()
    # productPrice = self.product.price
    # productTotalPrice = self.productQuantity * self.productPrice
    productName = models.CharField(max_length=100,null=True)
    productBatch = models.CharField(max_length=50,null=True)
    productPacking = models.CharField(max_length=50,null=True)
    productQuantity = models.IntegerField(default=1)
    productPrice = models.FloatField(default=0)
    productTotalPrice = models.FloatField(default=0) #self.productQuantity * self.productPrice

    def __str__(self):
        return "{}".format(self.purchaseno.purchaseno)
    
    def getProductName(self):
        return "Product Name: {}".format(self.bills.purchaseno)

class BillItemsTest(models.Model):
    purchaseno = models.ForeignKey(Bill, related_name="bills2", on_delete=models.CASCADE)
    # productName = self.product.batch_no.product.product
    # productBatch = self.product.batch_no.batch_no
    # productPacking = self.product.packing
    # productQuantity = models.IntegerField()
    # productPrice = self.product.price
    # productTotalPrice = self.productQuantity * self.productPrice
    productName = models.ForeignKey(ProductDetailBatch, related_name="bills2", on_delete=models.CASCADE)
    productBatch = models.CharField(max_length=50,null=True)
    productPacking = models.CharField(max_length=50,null=True)
    productQuantity = models.IntegerField(default=1)
    productPrice = models.FloatField(default=0)
    productTotalPrice = models.FloatField(default=0) #self.productQuantity * self.productPrice

    def __str__(self):
        return "{}".format(self.purchaseno.purchaseno)
    
    def getProductName(self):
        return "Product Name: {}".format(self.bills.purchaseno)


class BillTest2(models.Model):
    purchaseno = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE)
    purchase_date = models.DateField('purchase date')

    def __str__(self):
        return "{}_{}".format(self.customer.name,self.purchaseno)

class BillItemsTest2(models.Model):
    purchaseno = models.ForeignKey(BillTest2, related_name="bills22", on_delete=models.CASCADE)
    # productName = self.product.batch_no.product.product
    # productBatch = self.product.batch_no.batch_no
    # productPacking = self.product.packing
    # productQuantity = models.IntegerField()
    # productPrice = self.product.price
    # productTotalPrice = self.productQuantity * self.productPrice
    productName = models.ForeignKey(ProductDetailBatch, related_name="bills22", on_delete=models.CASCADE)
    productBatch = models.CharField(max_length=50,null=True)
    productPacking = models.CharField(max_length=50,null=True)
    productQuantity = models.IntegerField(default=1)
    productPrice = models.FloatField(default=0)
    productTotalPrice = models.FloatField(default=0) #self.productQuantity * self.productPrice

    def __str__(self):
        return "{}".format(self.purchaseno.purchaseno)
    
    def getProductName(self):
        return "Product Name: {}".format(self.bills.purchaseno)