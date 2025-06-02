from django.db import models

# Create your models here.

class CommonInfo(models.Model):
    date = models.DateField(auto_now_add=True)
    bill_no = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    yarn_lot = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    yarn_count = models.CharField(max_length=50)
    colour = models.CharField(max_length=50, null=True)
    no_of_cones = models.PositiveIntegerField()
    avg_cone_weight = models.DecimalField(max_digits=10, decimal_places=3)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3)
    net_weight = models.DecimalField(max_digits=6, decimal_places=3, editable=False, null=True)
    remarks = models.CharField(max_length=50, null=True, default="", blank=True)
    
    class Meta:
        abstract = True
        
    def calculate_net_weight(self):
        if self.gross_weight is not None:
            self.net_weight = self.gross_weight - (self.avg_cone_weight * self.no_of_cones)

    def save(self, *args, **kwargs):
        self.calculate_net_weight()
        super().save(*args, **kwargs)

class Receipt(CommonInfo, models.Model):
    PURCHASED_TYPE = {
             ('Imported','Imported'),
             ('Local','Local')
         }
    receipt_type = models.CharField(max_length=50, choices=PURCHASED_TYPE, default="", null=True) 
    
    def __str__(self):
       return f'{self.name}-{self.yarn_count}-{self.content}'

class Issued(CommonInfo, models.Model):
     def __str__(self):
        return f'{self.name}-{self.yarn_count}-{self.content}'

class Production_Issued(CommonInfo, models.Model):
    article = models.CharField(max_length=50)
    no_of_article = models.PositiveIntegerField()
    average_weight_of_article = models.DecimalField(max_digits=10, decimal_places=3)
    required_weight_for_prod = models.DecimalField(max_digits=10, decimal_places=3, editable=False, null=True)
    
    def __str__(self):
        return f'{self.name}-{self.yarn_count}-{self.content}'
    
    def save(self, *args, **kwargs):
        self.calculate_net_weight()  # From CommonInfo

        if self.no_of_article and self.average_weight_of_article:
            self.required_weight_for_prod = self.no_of_article * self.average_weight_of_article

        super().save(*args, **kwargs)
    
    
class Production_Return(models.Model):
    
    date = models.DateField(auto_now_add=True)
    bill_no = models.CharField(max_length=50)
    name = models.CharField(max_length=50, editable=False)
    yarn_lot = models.CharField(max_length=50, editable=False)
    content = models.CharField(max_length=50, editable=False)
    yarn_count = models.CharField(max_length=50, editable=False)
    colour = models.CharField(max_length=50, null=True, editable=False)
    no_of_cones = models.PositiveIntegerField()
    avg_cone_weight = models.DecimalField(max_digits=10, decimal_places=3)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3)
    net_weight = models.DecimalField(max_digits=6, decimal_places=3, editable=False, null=True)
    remarks = models.CharField(max_length=50, null=True, default="", blank=True)
    
    article = models.CharField(max_length=50, blank=True, editable=False)
    no_of_article = models.PositiveIntegerField(null=True, blank=True, editable=False)
    average_weight_of_article = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, editable=False)
    required_weight_for_prod = models.DecimalField(max_digits=10, decimal_places=3, editable=False, null=True)
    total_usage = models.DecimalField(max_digits=10, decimal_places=3, editable=False, null=True)
    yarn_wastage = models.DecimalField(max_digits=10, decimal_places=3, editable=False, null=True)
    no_of_returned_article = models.PositiveIntegerField(null=True)
    weight_of_returned_article =  models.DecimalField(max_digits=10, decimal_places=3, null=True)

    def __str__(self):
        return f'{self.name}-{self.yarn_count}-{self.content}'
    
    def save(self, *args, **kwargs):
        
            # Step 1: Calculate net weight of this return
        if self.gross_weight is not None:
            self.net_weight = self.gross_weight - (self.avg_cone_weight * self.no_of_cones)

        # Step 2: Fetch all Production_Issued entries with matching bill_no
        issued_entries = Production_Issued.objects.filter(bill_no=self.bill_no)
        
        
        from django.db.models import Sum
        total_issued = issued_entries.aggregate(Sum('net_weight'))['net_weight__sum'] or 0
        self.total_usage = total_issued - self.net_weight
        
        
        
        if issued_entries.exists():
            first_issued = issued_entries.first()

            # Copy fields from the first Production_Issued record
            self.name = first_issued.name
            self.yarn_lot = first_issued.yarn_lot
            self.content = first_issued.content
            self.yarn_count = first_issued.yarn_count
            self.colour = first_issued.colour

            self.article = first_issued.article
            self.no_of_article = first_issued.no_of_article
            self.average_weight_of_article = first_issued.average_weight_of_article
            
            
            if self.no_of_article and self.average_weight_of_article:
                self.required_weight_for_prod = self.no_of_article * self.average_weight_of_article
            
            self.yarn_wastage = self.total_usage - self.required_weight_for_prod
            
        super().save(*args, **kwargs)