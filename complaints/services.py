import logging
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def send_complaint_status_email(complaint, note=""):
    """Notifies the resident when complaint status shifts."""
    if not complaint.resident.email:
        logger.warning("No email on file for resident %s", complaint.resident.username)
        return

    subject = f"[SocietySync] Complaint #{complaint.id} Updated: {complaint.status}"
    message = (
        f"Hello {complaint.resident.first_name or complaint.resident.username},\n\n"
        f"Your complaint regarding '{complaint.category}' has been marked as: {complaint.status}.\n"
        f"Admin Note: {note or 'No specific note provided.'}\n\n"
        f"View real-time audit details: http://127.0.0.1:8000/complaint/{complaint.id}/\n\n"
        f"— Society Management"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[complaint.resident.email],
            fail_silently=False,
        )
    except Exception as exc:
        logger.error("Failed to send complaint status email: %s", exc)

def broadcast_important_notice(notice):
    """Broadcasts a high-priority notice to all registered resident emails."""
    recipient_list = list(
        User.objects.filter(is_active=True)
        .exclude(email="")
        .values_list('email', flat=True)
    )
    if not recipient_list:
        return

    subject = f"[URGENT NOTICE] {notice.title}"
    body = (
        f"Important Society Notice:\n\n"
        f"{notice.content}\n\n"
        f"Date: {notice.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        f"— SocietySync Admin"
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
    except Exception as exc:
        logger.error("Failed to broadcast notice email: %s", exc)