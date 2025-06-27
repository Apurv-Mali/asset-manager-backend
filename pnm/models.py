from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.contrib import admin
from django.db.models import F


ASSET_TYPE_CHOICES = [
    ('Tipper', 'Tipper'),
    ('Excavator', 'Excavator'),
    ('Paver','Paver'),
    ('Dozer','Dozer'),
    ('B-Tempo', 'B-Tempo'),
    ('Bus', 'Bus'),
    ('Camper','Camper'),
    ('Farana','Farana'),
    ('Grader', 'Grader'),
    ('Loader', 'Loader'),
    ('Backhoe Loader','Backhoe Loader'),
    ('Roller','Roller'),
    ('Service Van', 'Service Van'),
    ('Trailor', 'Trailor'),
    ('Transit Mixer','Transit Mixer'),
    ('Water Tanker','Water Tanker'),
    ('Wagon Drill','Wagon Drill'),
    ('Bitumen Bowser','Bitumen Bowser'),
    ('Diesel Tanker','Diesel Tanker'),
    ('Personal Vehicle','Personal Vehicle'),
    ('Two Wheeler','Two Wheeler'),
    ('Pick Up','Pick Up'),
    ('Crane','Crane'),
    
]

DEAL_TYPE_CHOICES = [
    ('Sale', 'Sale'),
    ('Purchase', 'Purchase'),
    ('Shifting', 'Shifting'),
]

BREAKDOWN_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Partially Completed', 'Partially Completed'),
    ('Completed', 'Completed'),
]

NOTIFICATION_TYPE_CHOICES = [
    ('trip', 'Trip Update'),
    ('diesel', 'Diesel Entry'),
    ('breakdown', 'Breakdown'),
    ('general', 'General'),
]

ASSET_CATEGORY = [
    ('vehicle','vehicle'),
    ('machinery','machinery')
]

# Asset Model
class Asset(models.Model):
    asset_id = models.CharField(max_length=50, unique=True)
    registration_no = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=ASSET_TYPE_CHOICES)
    owner = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=ASSET_CATEGORY)
    purchase_value = models.IntegerField()
    purchase_date = models.DateField()
    chasis_no = models.CharField(max_length=30)
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2)
    emi_provider = models.CharField(max_length=100)
    emi_payment_date = models.DateField(null=True)
    emi_start_date = models.DateField(null=True)
    emi_end_date = models.DateField(null=True)
    insurance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    insurance_provider = models.CharField(max_length=100)
    insurance_validity = models.DateField(null=True)
    puc_amount = models.DecimalField(max_digits=10, decimal_places=2)
    puc_start_date = models.DateField()
    puc_end_date = models.DateField()
    ot_road_tax = models.BooleanField()
    fitness_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fitness_start_date = models.DateField(null=True)
    fitness_end_date = models.DateField(null=True)
    road_tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    road_tax_start_date = models.DateField(null=True)
    road_tax_end_date = models.DateField(null=True)
    permit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    permit_start_date = models.DateField()
    permit_end_date = models.DateField()
    rate_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_hr = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_shift = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    charges = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.registration_no})"

# Manager Model
class Manager(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    salary = models.IntegerField(null=True)
    grade = models.CharField(max_length=10)
    sub_grade = models.CharField(max_length=10)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        if user:
            user.delete()

    def __str__(self):
        return self.name
    
    @admin.display(ordering='user__first_name')
    
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

# Mechanic Model
class Mechanic(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    salary = models.IntegerField(null=True)
    grade = models.CharField(max_length=10)
    sub_grade = models.CharField(max_length=10)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        if user:
            user.delete()

    def __str__(self):
        return self.name 

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    

# AssetManager Model
class AssetManager(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='asset_assignments')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    site = models.CharField(max_length=255)
    date_assigned = models.DateTimeField(auto_now=True)

# Trip Details Model
class TripDetails(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='trips')  
    date = models.DateTimeField(auto_now=True)
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255, null=True)
    material = models.CharField(max_length=255, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    distance = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    deal_type = models.CharField(max_length=50, choices=DEAL_TYPE_CHOICES)
    hours = models.IntegerField(null=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True)
    receiver = models.ForeignKey(Manager,on_delete=models.CASCADE,null=True,related_name='trip_receiver')
    shift = models.IntegerField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    operator = models.ForeignKey('Operator', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Trip on {self.date} - {self.asset.name}"

# Diesel Entry Model
class DieselEntry(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)  
    date = models.DateTimeField(auto_now=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    previous_reading = models.DecimalField(max_digits=10, decimal_places=2)
    reading = models.DecimalField(max_digits=10, decimal_places=2)  
    site = models.CharField(max_length=255)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Diesel Entry on {self.date} - {self.asset.name}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only on create
            latest_stock_entry = DieselStock.objects.order_by('-id').first()
            if latest_stock_entry:
                # Reduce the quantity from latest_stock
                latest_stock_entry.quantity -= self.quantity
                latest_stock_entry.amount = latest_stock_entry.quantity * latest_stock_entry.rate
                # Recalculate its stock based on previous
                prev_stock_entry = DieselStock.objects.filter(id__lt=latest_stock_entry.id).order_by('-id').first()
                latest_stock_entry.stock = (prev_stock_entry.stock if prev_stock_entry else 0) + latest_stock_entry.quantity
                latest_stock_entry.save()

                # Recalculate all subsequent stock entries
                following = DieselStock.objects.filter(id__gt=latest_stock_entry.id).order_by('id')
                running_stock = latest_stock_entry.stock
                for entry in following:
                    running_stock += entry.quantity
                    entry.stock = running_stock
                    entry.save()

        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        # Restore quantity back to the latest DieselStock entry
        latest_stock_entry = DieselStock.objects.order_by('-id').first()
        if latest_stock_entry:
            # Add quantity back
            latest_stock_entry.quantity += self.quantity
            latest_stock_entry.amount = latest_stock_entry.quantity * latest_stock_entry.rate

            # Recalculate stock based on previous entry
            prev_stock_entry = DieselStock.objects.filter(id__lt=latest_stock_entry.id).order_by('-id').first()
            latest_stock_entry.stock = (prev_stock_entry.stock if prev_stock_entry else 0) + latest_stock_entry.quantity
            latest_stock_entry.save()

            # Update all following stock entries
            following = DieselStock.objects.filter(id__gt=latest_stock_entry.id).order_by('id')
            running_stock = latest_stock_entry.stock
            for entry in following:
                running_stock += entry.quantity
                entry.stock = running_stock
                entry.save()

        super().delete(*args, **kwargs)

# Breakdown Model
class Breakdown(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='breakdown_occurred')  
    date = models.DateTimeField(auto_now=True)
    site = models.CharField(max_length=255)
    issue = models.TextField()
    action_taken = models.TextField(null=True)
    estimated_delivery_date = models.DateField(null=True)
    delivered_at_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=BREAKDOWN_STATUS_CHOICES, default='Pending')
    cost = models.IntegerField(null=True)
    manpower_cost = models.IntegerField(null=True)
    material_used = models.CharField(max_length=255,null=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return f"Breakdown on {self.date} - {self.asset.name}"

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES, default='general')  
    created_at = models.DateTimeField(auto_now_add=True)  
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.notification_type}"

    def mark_as_read(self):
        """Method to mark a notification as read."""
        self.is_read = True
        self.save()

class DieselStock(models.Model):

    challan_no = models.IntegerField(unique=True)
    date = models.DateField(auto_now_add=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    party_name = models.CharField(max_length=255)
    stock = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.rate

        if self.pk:
            # Editing existing entry
            old = DieselStock.objects.get(pk=self.pk)

            # Get previous stock from the entry just before this one
            prev_stock_entry = DieselStock.objects.filter(id__lt=self.pk).order_by('-id').first()
            prev_stock = prev_stock_entry.stock if prev_stock_entry else 0

            # Update current stock
            self.stock = prev_stock + self.quantity

            # Save current record first
            super().save(*args, **kwargs)

            # Now update all following entries
            entries = DieselStock.objects.filter(id__gt=self.pk).order_by('id')
            running_stock = self.stock
            for entry in entries:
                running_stock += entry.quantity
                entry.stock = running_stock
                entry.save()
        else:
            # New entry
            last_entry = DieselStock.objects.order_by('-id').first()
            prev_stock = last_entry.stock if last_entry else 0
            self.stock = prev_stock + self.quantity
            super().save(*args, **kwargs)

class Operator(models.Model):
    name = models.CharField(max_length=244)
    role = models.CharField(max_length=244)
    type = models.CharField(max_length=244)
    salary = models.IntegerField()
    grade = models.CharField(max_length=10)
    sub_grade = models.CharField(max_length=10)
    phone = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.name

class MonthlyRent(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now=True)
    rate_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_hr = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_shift = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    charges= models.DecimalField(max_digits=10, decimal_places=2)
