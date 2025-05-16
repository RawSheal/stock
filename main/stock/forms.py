from django import forms
from django.forms import ModelForm
from .models import Receipt, Issued, Production_Issued, Production_Return

class Receipt_Form(ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
        
class Issued_Form(ModelForm):
    class Meta:
        model = Issued
        fields = '__all__'
        
class Production_Issued_Form(ModelForm):
    class Meta:
        model = Production_Issued
        fields = '__all__'
        
class Production_Return_Form(ModelForm):
    class Meta:
        model = Production_Return
        fields = '__all__'