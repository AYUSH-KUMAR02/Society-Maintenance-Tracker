from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Complaint, StatusHistory, Notice
from .services import send_complaint_status_email, broadcast_important_notice

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'resident', 'category', 'status', 'priority', 'created_at', 'overdue_flag')
    list_filter = ('status', 'category', 'priority', 'created_at')
    search_fields = ('description', 'resident__username')
    fields = ('resident', 'category', 'description', 'photo', 'status', 'priority', 'admin_note')

    def overdue_flag(self, obj):
        if obj.is_overdue():
            return mark_safe('<span style="color:red; font-weight:bold;">⚠️ OVERDUE</span>')
        return "No"
    overdue_flag.short_description = "Overdue"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change and 'status' in form.changed_data:
            send_complaint_status_email(obj, note=obj.admin_note)

    def changelist_view(self, request, extra_context=None):
        counts = Complaint.objects.all()
        overdue_count = sum(1 for c in counts if c.is_overdue())
        extra_context = extra_context or {}
        extra_context['metrics'] = {
            'Open': counts.filter(status='Open').count(),
            'In_Progress': counts.filter(status='In Progress').count(),
            'Resolved': counts.filter(status='Resolved').count(),
            'Overdue': overdue_count,
        }
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_important', 'created_at')

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if obj.is_important and (is_new or 'is_important' in form.changed_data):
            broadcast_important_notice(obj)

admin.site.register(StatusHistory)