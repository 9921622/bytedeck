from django.db import models

from django.apps import apps
from taggit.managers import TaggableManager


def total_xp_by_tags(user, tags: list):
    """ 
        Returns user's total xp over active_semester filtered by tags
    """ 
    # get models through here to prevent circular imports
    Quest = apps.get_model("quest_manager", "Quest")
    QuestSubmission = apps.get_model("quest_manager", "QuestSubmission")
    Badge = apps.get_model("badges", "Badge")
    BadgeAssertion = apps.get_model("badges", "BadgeAssertion")

    # get all objects with xp that is related to user
    # convert submission/assertion qs into Quest/Badge qs
    xpitems = [
        Quest.objects.filter(id__in=[qs.quest.id for qs in QuestSubmission.objects.all_completed(user=user)], tags__name__in=tags).distinct(), 
        Badge.objects.filter(id__in=[ba.badge.id for ba in BadgeAssertion.objects.all_for_user(user=user)], tags__name__in=tags).distinct(),
    ]

    return sum(obj.xp for qs in xpitems for obj in qs)


class TagsModelMixin(models.Model):
    """And abstract model to implement tags"""

    tags = TaggableManager(blank=True)

    class Meta:
        abstract = True
