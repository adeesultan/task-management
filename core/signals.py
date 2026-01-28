from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from django.core.mail import send_mail
from django.conf import settings

from .models import Task, TaskActivityLog


logger = logging.getLogger("tasks")


@receiver(post_save, sender=Task)
def create_task_activity(sender, instance, created, **kwargs):
    if not created:
        return

    # 1. Create activity log (core behavior; failure is logged but we continue)
    try:
        TaskActivityLog.objects.create(
            task=instance,
            message=f"Task created with title: {instance.title}",
        )
    except Exception:
        logger.exception(
            "TaskActivityLog create failed | task_id=%s",
            instance.id,
        )
        return

    # 2. Log task creation (always, so we have a record even if email fails later)
    logger.info(
        "Task created | task_id=%s | title='%s' | project_id=%s | assigned_to=%s",
        instance.id,
        instance.title,
        instance.project_id,
        instance.assigned_to_id,
    )

    # 3. Send email only when assigned user has email; failures don't affect log or logging
    if not (instance.assigned_to and instance.assigned_to.email):
        logger.info(
            "Email skipped | task_id=%s | reason=no assigned user or email",
            instance.id,
        )
        return

    try:
        send_mail(
            subject="New Task Assigned",
            message=(
                f"Hello {instance.assigned_to.get_full_name() or instance.assigned_to.username},\n\n"
                f"You have been assigned a new task.\n\n"
                f"Title: {instance.title}\n"
                f"Project: {instance.project.name}\n"
                f"Due Date: {instance.due_date}\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.assigned_to.email],
            fail_silently=False,
        )
        logger.info(
            "Email sent | task_id=%s | recipient=%s",
            instance.id,
            instance.assigned_to.email,
        )
    except Exception:
        logger.exception(
            "Task assignment email failed | task_id=%s | recipient=%s",
            instance.id,
            instance.assigned_to.email,
        )
