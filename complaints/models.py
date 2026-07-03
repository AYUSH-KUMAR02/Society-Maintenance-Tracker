from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

CATEGORIES = [('Plumbing', 'Plumbing'), ('Electrical', 'Electrical'), ('Security', 'Security'), ('Other', 'Other')]
STATUS_CHOICES = [('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved')]
PRIORITIES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]

class Complaint(models.Model):
    resident = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField()
    photo = models.ImageField(upload_to='complaints/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    priority = models.CharField(max_length=10, choices=PRIORITIES, default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_note = models.TextField(blank=True, null=True)

    def is_overdue(self, days=3): # Configurable threshold
        return self.status != 'Resolved' and (timezone.now() - self.created_at).days >= days

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = Complaint.objects.get(pk=self.pk).status if not is_new else None
        super().save(*args, **kwargs)
        
        if is_new or old_status != self.status:
            StatusHistory.objects.create(complaint=self, status=self.status, note=self.admin_note or "Status updated")

class StatusHistory(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    note = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)