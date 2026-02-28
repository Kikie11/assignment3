from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from simple_history.models import HistoricalRecords

# TOPIC 1: Custom User Models
class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrator'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')

    @property
    def is_manager_or_admin(self):
        return self.role in ['ADMIN', 'MANAGER'] or self.is_superuser

# TOPIC 2: Abstract Base Classes (Code Reuse)
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created' and 'modified' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Asset(TimeStampedModel):
    """
    Concrete model inheriting from TimeStampedModel.
    """
    ASSET_TYPES = (
        ('LAPTOP', 'Laptop'),
        ('MONITOR', 'Monitor'),
        ('PHONE', 'Phone'),
        ('FURNITURE', 'Furniture'),
    )

    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    # DecimalField is best practice for currency/value
    cost = models.DecimalField(max_digits=10, decimal_places=2) 
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')

    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"

class MaintenanceLog(models.Model):
    """
    Tracks repairs and maintenance performed on specific assets.
    One-to-Many relationship: one Asset can have many MaintenanceLogs.
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_logs')
    service_date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Maintenance on {self.asset.name} - {self.service_date}"

    class Meta:
        ordering = ['-service_date']