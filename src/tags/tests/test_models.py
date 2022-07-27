from django_tenants.test.cases import TenantTestCase
from django.contrib.auth import get_user_model

from model_bakery import baker

from tags.models import total_xp_by_tags
from siteconfig.models import SiteConfig
from quest_manager.models import Quest, QuestSubmission
from badges.models import Badge, BadgeAssertion

import random
import itertools

User = get_user_model()


class Tag_total_xp_by_tags_Tests(TenantTestCase):
    """ 
        Specialized TestClass for testing total_xp_by_tags function
    """ 

    def setUp(self):
        self.user = baker.make(User)
        self.random = random.Random(9921622)

    def create_quest(self, xp):
        quest = baker.make(Quest, xp=xp)
        qs = baker.make(
            QuestSubmission, 
            quest=quest, 
            user=self.user, 
            is_completed=True, 
            is_approved=True, 
            semester=SiteConfig().get().active_semester,
        )

        return quest, qs

    def create_badge(self, xp):
        badge = baker.make(Badge, xp=xp)
        ba = baker.make(BadgeAssertion, badge=badge, user=self.user)

        return badge, ba

    # QUEST ONLY TESTS

    def test_one_tag_quests_only(self):
        """ 
            See if correct xp is displayed using only 1 tag added to Quest objects
        """ 
        xp_list = [self.random.randint(0, 100) for i in range(10)]
        xp_iter = itertools.cycle(xp_list)
        
        for i in range(len(xp_list)):
            quest, _ = self.create_quest(next(xp_iter))
            quest.tags.add("TAG")

        self.assertEqual(total_xp_by_tags(self.user, ["TAG"]), sum(xp_list))

    def test_multiple_separate_tags_quests_only(self):
        """ 
            See if correct xp is displayed using only multiple tags added to Quest objects
            only 1 unique tag per quest
        """ 
        tag_list = [f"tag-{i}" for i in range(5)]
        xp_list = [self.random.randint(0, 100) for i in range(5 * len(tag_list))]
        xp_iter = itertools.cycle(xp_list)

        for tag_el in tag_list:
            for i in range(len(xp_list) // len(tag_list)):
                quest, _ = self.create_quest(next(xp_iter))
                quest.tags.add(tag_el)

        self.assertEqual(total_xp_by_tags(self.user, tag_list), sum(xp_list))

    def test_multiple_crossing_tags_quests_only(self):
        """ 
            See if correct xp is displayed using only multiple tags added to Quest objects
            each quest object should have multiple tags
        """ 
        tag_list = [(f"tag0-{i}", f"tag1-{i}") for i in range(5)]
        xp_list = [self.random.randint(0, 100) for i in range(5 * len(tag_list))]
        xp_iter = itertools.cycle(xp_list)

        for tag_set in tag_list:
            for i in range(len(xp_list) // len(tag_list)):
                quest, _ = self.create_quest(next(xp_iter))
                quest.tags.add(tag_set[0])
                quest.tags.add(tag_set[1])

        unpacked_tag_list = [tag_set[index] for tag_set in tag_list for index in range(len(tag_set))]
        self.assertEqual(total_xp_by_tags(self.user, unpacked_tag_list), sum(xp_list))

    # BADGE ONLY TESTS

    def test_one_tag_badges_only(self):
        """ 
            See if correct xp is displayed using only 1 tag added to Badge objects
        """ 
        xp_list = [self.random.randint(0, 100) for i in range(10)]
        xp_iter = itertools.cycle(xp_list)
        
        for i in range(len(xp_list)):
            badge, _ = self.create_badge(next(xp_iter))
            badge.tags.add("TAG")

        self.assertEqual(total_xp_by_tags(self.user, ["TAG"]), sum(xp_list))

    def test_multiple_separate_tags_badges_only(self):
        """ 
            See if correct xp is displayed using only multiple tags added to Badge objects
            only 1 unique tag per badge
        """ 
        tag_list = [f"tag-{i}" for i in range(5)]
        xp_list = [self.random.randint(0, 100) for i in range(5 * len(tag_list))]
        xp_iter = itertools.cycle(xp_list)

        for tag_el in tag_list:
            for i in range(len(xp_list) // len(tag_list)):
                badge, _ = self.create_badge(next(xp_iter))
                badge.tags.add(tag_el)

        self.assertEqual(total_xp_by_tags(self.user, tag_list), sum(xp_list))

    def test_multiple_crossing_tags_badges_only(self):
        """ 
            See if correct xp is displayed using only multiple tags added to Badge objects
            each Badge object should have multiple tags
        """ 
        tag_list = [(f"tag0-{i}", f"tag1-{i}") for i in range(5)]
        xp_list = [self.random.randint(0, 100) for i in range(5 * len(tag_list))]
        xp_iter = itertools.cycle(xp_list)

        for tag_set in tag_list:
            for i in range(len(xp_list) // len(tag_list)):
                badge, _ = self.create_badge(next(xp_iter))
                badge.tags.add(tag_set[0])
                badge.tags.add(tag_set[1])

        unpacked_tag_list = [tag_set[index] for tag_set in tag_list for index in range(len(tag_set))]
        self.assertEqual(total_xp_by_tags(self.user, unpacked_tag_list), sum(xp_list))

    # QUEST + BADGE TESTS

    def test_one_tag_quests_badges(self):
        """ 
            See if correct xp is displayed using only 1 tag added to Quest and Badge objects
        """ 
        xp_list = [self.random.randint(0, 100) for i in range(10 * 2)]
        xp_iter = itertools.cycle(xp_list)
        
        for i in range(len(xp_list) // 2):
            quest, _ = self.create_quest(next(xp_iter))
            quest.tags.add("TAG")

            badge, _ = self.create_badge(next(xp_iter))
            badge.tags.add("TAG")

        self.assertEqual(total_xp_by_tags(self.user, ["TAG"]), sum(xp_list))

    def test_multiple_separate_tags_quests_badges(self):
        """ 
            See if correct xp is displayed using only multiple tags added to Quest and Badge objects
            only 1 unique tag per quest and badge
        """ 
        tag_list = [f"tag-{i}" for i in range(5 * 2)]
        xp_list = [self.random.randint(0, 100) for i in range(5 * len(tag_list))]
        xp_iter = itertools.cycle(xp_list)

        for tag_el in tag_list:
            for i in range(len(xp_list) // len(tag_list)):

                if i % 2 == 0:
                    quest, _ = self.create_quest(next(xp_iter))
                    quest.tags.add(tag_el)
                else:
                    badge, _ = self.create_badge(next(xp_iter))
                    badge.tags.add(tag_el)

        self.assertEqual(total_xp_by_tags(self.user, tag_list), sum(xp_list))

    def test_multiple_crossing_tags_quest_badges(self):
        """ 
            See if correct xp is displayed using only multiple tags added to Quest and Badge objects
            each Quest and Badge object should have multiple tags
        """ 
        tag_list = [(f"tag0-{i}", f"tag1-{i}") for i in range(5 * 2)]
        xp_list = [self.random.randint(0, 100) for i in range(5 * len(tag_list))]
        xp_iter = itertools.cycle(xp_list)

        for tag_set in tag_list:
            for i in range(len(xp_list) // len(tag_list)):
                
                if i % 2 == 0:
                    quest, _ = self.create_quest(next(xp_iter))
                    quest.tags.add(tag_set[0])
                    quest.tags.add(tag_set[1])
                else:
                    badge, _ = self.create_badge(next(xp_iter))
                    badge.tags.add(tag_set[0])
                    badge.tags.add(tag_set[1])

        unpacked_tag_list = [tag_set[index] for tag_set in tag_list for index in range(len(tag_set))]
        self.assertEqual(total_xp_by_tags(self.user, unpacked_tag_list), sum(xp_list))
