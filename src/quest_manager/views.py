from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.template import RequestContext, loader
from .forms import QuestForm
from .models import Quest
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

@login_required
def quest_list(request):
    # quest_list = Quest.objects.order_by('name')
    quest_list = Quest.objects.get_active()
    # output = ', '.join([p.name for p in quest_list])
    context = {
        "title": "Quests",
        "heading": "Quests",
        "quest_list": quest_list,
    }
    return render(request, "quest_manager/quests.html" , context)

def quest_create(request):
    form =  QuestForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('quests:quests')
    context = {
        "title": "Quests",
        "heading": "Create New Quest",
        "form": form,
        "submit_btn_value": "Create",
    }
    return render(request, "quest_manager/quest_form.html", context)

def quest_update(request, quest_id):
    quest_to_update = get_object_or_404(Quest, pk=quest_id)
    form = QuestForm(request.POST or None, instance = quest_to_update)
    if form.is_valid():
        form.save()
        return redirect('quests:quests')
    context = {
        "title": "Quests",
        "heading": "Update Quest",
        "form": form,
        "submit_btn_value": "Update",
    }
    return render(request, "quest_manager/quest_form.html", context)

def quest_copy(request, quest_id):
    new_quest = get_object_or_404(Quest, pk=quest_id)
    new_quest.pk = None # autogen a new primary key (quest_id by default)
    new_quest.name = "Copy of " + new_quest.name
    # print(quest_to_copy)
    # print(new_quest)
    # new_quest.save()

    form =  QuestForm(request.POST or None, instance = new_quest)
    if form.is_valid():
        form.save()
        return redirect('quests:quests')
    context = {
        "title": "Quests",
        "heading": "Copy a Quest",
        "form": form,
        "submit_btn_value": "Create",
    }
    return render(request, "quest_manager/quest_form.html", context)

# @login_required
# def copy(request, quest_id):
#     title = "Quests"
#
#     q = get_object_or_404(Quest, pk=quest_id)
#
#
#
#     context = {
#         "title": title,
#         "heading": ("Copy: %s" % q.name),
#         "q": q2,
#     }
#     return render(request, 'quest_manager/detail.html', context)

# @login_required
# def update(request, quest_id):
#     title = "Quests"
#     template_name = ""
#     q = get_object_or_404(Quest, pk=quest_id)
#
#
#
#     context = {
#         "title": title,
#         "heading": ("Copy: %s" % q.name),
#         "q": q,
#     }
#     return render(request, template_name, context)

@login_required
def detail(request, quest_id):
    title = "Quests"
    heading = "Quest Detail"

    q = get_object_or_404(Quest, pk=quest_id)

    context = {
        "title": title,
        "heading": ("Quest: %s" % q.name),
        "q": q,
    }
    return render(request, 'quest_manager/detail.html', context)

## Demo of sending email
# @login_required
# def email_demo(request):
#     subject = "Test email from Hackerspace Online"
#     from_email = ("Timberline's Digital Hackerspace <" +
#         settings.EMAIL_HOST_USER +
#         ">")
#     to_emails = [from_email]
#     email_message = "from %s: %s via %s" %(
#         "Dear Bloggins", "sup", from_email)
#
#     html_email_message = "<h1> if this is showing you received an HTML messaage</h1>"
#
#     send_mail(subject,
#         email_message,
#         from_email,
#         to_emails,
#         html_message = html_email_message,
#         fail_silently=False)
#
#     context = {
#         "email_to" : to_emails,
#         "email_from": from_email,
#         "email_message":email_message,
#         "html_email_message": html_email_message
#
#     }
#
#     return render(request, "email_demo.html", context)


##
