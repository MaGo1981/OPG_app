from django.contrib import admin
from .models import Product
from .models import ProductCategory
from .models import Profile
from .models import Opg


admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Profile)
admin.site.register(Opg)
