import os
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from complaints.models import Complaint

class Command(BaseCommand):
    help = "Checks open complaints past the threshold and alerts administrators"

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=3, help='Threshold days before overdue')

    def handle(self, *args, **options):
        threshold_days = options['days']
        overdue_tickets = [c for c in Complaint.objects.exclude(status='Resolved') if c.is_overdue(days=threshold_days)]

        self.stdout.write(f"Scanned complaints. Found {len(overdue_tickets)} overdue tickets.")

        if overdue_tickets:
            summary = "\n".join([f"- Ticket #{c.id} ({c.category}) filed by {c.resident.username} on {c.created_at.strftime('%Y-%m-%d')}" for c in overdue_tickets])
            admin_email = os.getenv('EMAIL_HOST_USER')
            if admin_email:
                send_mail(
                    subject=f"[SocietySync Alert] {len(overdue_tickets)} Overdue Maintenance Tickets",
                    message=f"The following tickets have exceeded {threshold_days} days without resolution:\n\n{summary}\n\nReview them in the admin dashboard: http://127.0.0.1:8000/admin/complaints/complaint/",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin_email],
                    fail_silently=True
                )