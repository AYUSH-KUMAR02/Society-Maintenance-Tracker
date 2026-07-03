from django.contrib import admin
from django.core.mail import send_mail
from django.utils.html import format_html
from .models import Complaint, StatusHistory, Notice

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'resident', 'category', 'status', 'priority', 'created_at', 'overdue_flag')
    list_filter = ('status', 'category', 'priority', 'created_at')
    search_fields = ('description', 'resident__username')
    fields = ('resident', 'category', 'description', 'photo', 'status', 'priority', 'admin_note')
    
    def overdue_flag(self, obj):
        return format_html('<span style="color:red; font-weight:bold;">⚠️ OVERDUE</span>') if obj.is_overdue() else "No"
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change and 'status' in form.changed_data:
            send_mail(
                f"Complaint #{obj.id} Update",
                f"Your complaint status is now: {obj.status}.\nNote: {obj.admin_note}",
                'admin@society.com', [obj.resident.email]
            )

    def changelist_view(self, request, extra_context=None):
        # Inject custom dashboard metrics straight into the list view template context
        counts = Complaint.objects.all()
        overdue_count = sum(1 for c in counts if c.is_overdue())
        extra_context = extra_context or {}
        extra_context['metrics'] = {
            'Open': counts.filter(status='Open').count(),
            'In_Progress': counts.filter(status='In Progress').count(),
            'Resolved': counts.filter(status='Resolved').count(),
            'Overdue': overdue_count
        }
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_important', 'created_at')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_important:
            from django.contrib.auth.models import User
            emails = list(User.objects.values_list('email', flat=True))
            send_mail("IMPORTANT NOTICE", obj.content, 'admin@society.com', emails)

admin.site.register(StatusHistory)