from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone

from announcements.models import Announcement
from courses.models import CourseStudent
from hackerspace_online.celery import app
from notifications.signals import notify
from siteconfig.models import SiteConfig
from profile_manager.models import Profile

User = get_user_model()


@app.task(name='announcements.tasks.send_notifications')
def send_notifications(user_id, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    sending_user = User.objects.get(id=user_id)
    affected_users = CourseStudent.objects.all_users_for_active_semester()
    notify.send(
        sending_user,
        # action=new_announcement,
        target=announcement,
        recipient=sending_user,
        affected_users=affected_users,
        icon="<i class='fa fa-lg fa-fw fa-newspaper-o text-info'></i>",
        verb='posted'
    )


@app.task(name='announcements.tasks.send_announcement_emails')
def send_announcement_emails(content, root_url, absolute_url):
    siteconfig = SiteConfig.get()
    subject = f'{siteconfig.site_name_short} Announcement'
    text_content = content
    html_template = get_template('announcements/email_announcement.html')
    html_content = html_template.render({
        'content': content,
        'absolute_url': absolute_url,
        'root_url': root_url,
        'config': siteconfig,
        'profile_edit_url': reverse('profiles:profile_edit_own')
    })

    profile_emails = Profile.objects.get_mailing_list(as_emails_list=True, for_announcement_email=True)

    email_msg = EmailMultiAlternatives(
        subject,
        body=text_content,
        to=['contact@bytedeck.com'],
        bcc=profile_emails,
    )
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()

    return profile_emails
    # print("Sending {} announcement emails.".format(len(users_to_email)))


@app.task(name='announcements.tasks.publish_announcement')
def publish_announcement(user_id, announcement_id, root_url):
    """ Publish the announcement, including:
            - edit model instance
            - push notifications
            - send announcement emails
    """
    # update model instance
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    announcement.datetime_released = timezone.now()
    announcement.draft = False
    announcement.auto_publish = False
    announcement.full_clean()
    announcement.save()

    absolute_url = announcement.get_absolute_url()

    # push notifications
    send_notifications.apply_async(args=[user_id, announcement_id], queue='default')

    # Send the announcements by email to those who have ask for them, using celery
    send_announcement_emails.apply_async(args=[announcement.content, root_url, absolute_url], queue='default')
    # Email not set up anyway
