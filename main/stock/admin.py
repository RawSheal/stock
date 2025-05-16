from django.contrib import admin
from .models import Receipt, Issued, Production_Issued, Production_Return
# Register your models here.
admin.site.register(Receipt)
admin.site.register(Issued)
admin.site.register(Production_Issued)
admin.site.register(Production_Return)
