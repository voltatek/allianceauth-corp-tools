from unittest import mock
from django.test import TestCase
from allianceauth.tests.auth_utils import AuthUtils
from allianceauth.eveonline.models import EveCharacter, EveAllianceInfo, EveCorporationInfo
from allianceauth.authentication.models import CharacterOwnership
from django.utils import timezone
from datetime import timedelta
from corptools import models as ct_models
from django.contrib.auth.models import User, Group
from django.core.cache import cache


class TestSecGroupBotFilters(TestCase):
    @classmethod
    def setUpTestData(cls):

        ct_models.CharacterAudit.objects.all().delete()
        EveCharacter.objects.all().delete()
        User.objects.all().delete()
        CharacterOwnership.objects.all().delete()
        ct_models.EveLocation.objects.all().delete()
        ct_models.MapRegion.objects.all().delete()
        ct_models.MapConstellation.objects.all().delete()
        ct_models.MapSystem.objects.all().delete()
        ct_models.MapSystem.objects.all().delete()
        ct_models.Skill.objects.all().delete()

        userids = range(1, 11)

        cls.test_group, _ = Group.objects.update_or_create(name="Test_Group")

        users = []
        characters = []
        for uid in userids:
            user = AuthUtils.create_user(f"User_{uid}")
            main_char = AuthUtils.add_main_character_2(user,
                                                       f"Main {uid}",
                                                       uid,
                                                       corp_id=1,
                                                       corp_name='Test Corp 1',
                                                       corp_ticker='TST1')
            CharacterOwnership.objects.create(
                user=user, character=main_char, owner_hash=f"main{uid}")

            characters.append(main_char)
            users.append(user)
        cls.c1t1 = ct_models.CharacterTitle.objects.create(corporation_id=1,
                                                           corporation_name='Test Corp 1',
                                                           title="Test Title1",
                                                           title_id=1)

        cls.c1t2 = ct_models.CharacterTitle.objects.create(corporation_id=1,
                                                           corporation_name='Test Corp 1',
                                                           title="Test Title2",
                                                           title_id=2)

        # add some extra characters to users in 2 corps/alliance
        for uid in range(0, 5):  # test corp 2
            character = EveCharacter.objects.create(character_name=f'Alt {uid}',
                                                    character_id=11+uid,
                                                    corporation_name='Test Corp 2',
                                                    corporation_id=2,
                                                    corporation_ticker='TST2')
            CharacterOwnership.objects.create(character=character,
                                              user=users[uid],
                                              owner_hash=f'ownalt{11+uid}')
            characters.append(character)

        cls.c2t1 = ct_models.CharacterTitle.objects.create(corporation_id=2,
                                                           corporation_name='Test Corp 2',
                                                           title="Test Title1",
                                                           title_id=1)

        cls.c2t2 = ct_models.CharacterTitle.objects.create(corporation_id=2,
                                                           corporation_name='Test Corp 2',
                                                           title="Test Title2",
                                                           title_id=2)

        for uid in range(5, 10):  # Test alliance 1
            character = EveCharacter.objects.create(character_name=f'Alt {uid}',
                                                    character_id=11+uid,
                                                    corporation_name='Test Corp 3',
                                                    corporation_id=3,
                                                    corporation_ticker='TST3',
                                                    alliance_id=1,
                                                    alliance_name="Test Alliance 1",
                                                    alliance_ticker="TSTA1")
            CharacterOwnership.objects.create(character=character,
                                              user=users[uid],
                                              owner_hash=f'ownalt{11+uid}')
            characters.append(character)

        cls.alli = EveAllianceInfo.objects.create(alliance_id=1,
                                                  alliance_name="Test Alliance 1",
                                                  alliance_ticker="TSTA1",
                                                  executor_corp_id=3)

        cls.corp = EveCorporationInfo.objects.create(corporation_id=3,
                                                     corporation_name="Test Corp 3",
                                                     corporation_ticker="TST3",
                                                     member_count=10,
                                                     alliance=cls.alli,)

        # add some systems
        r1 = ct_models.MapRegion.objects.create(name="Test region 1",
                                                description="This region is junk at best, nothing is even in range",
                                                region_id=1)
        r2 = ct_models.MapRegion.objects.create(name="Test region 2",
                                                description="This region is a flood plain",
                                                region_id=2)
        r3 = ct_models.MapRegion.objects.create(name="Test region 3",
                                                description="This region is a fortress",
                                                region_id=3)
        c1 = ct_models.MapConstellation.objects.create(name="Test Constellation 1",
                                                       constellation_id=1,
                                                       region=r1)
        c2 = ct_models.MapConstellation.objects.create(name="Test Constellation 2",
                                                       constellation_id=2,
                                                       region=r2)
        c3 = ct_models.MapConstellation.objects.create(name="Test Constellation 3",
                                                       constellation_id=3,
                                                       region=r3)
        s1 = ct_models.MapSystem.objects.create(name="Test System 1",
                                                system_id=1,
                                                security_status=0.0,
                                                x=1,
                                                y=1,
                                                z=1,
                                                security_class="g",
                                                star_id=1,
                                                constellation=c1)
        s2 = ct_models.MapSystem.objects.create(name="Test System 2",
                                                system_id=2,
                                                security_status=0.0,
                                                x=1,
                                                y=1,
                                                z=1,
                                                security_class="g",
                                                star_id=2,
                                                constellation=c2)
        s3 = ct_models.MapSystem.objects.create(name="Test System 3",
                                                system_id=3,
                                                security_status=0.0,
                                                x=1,
                                                y=1,
                                                z=1,
                                                security_class="g",
                                                star_id=3,
                                                constellation=c3)

        audits = []
        for uid in range(0, 17):  # 4,5,6,7
            audits.append(ct_models.CharacterAudit.objects.create(character=characters[uid],
                                                                  last_update_assets=timezone.now(),
                                                                  last_update_clones=timezone.now(),
                                                                  last_update_pub_data=timezone.now(),
                                                                  last_update_skill_que=timezone.now(),
                                                                  last_update_skills=timezone.now(),
                                                                  last_update_wallet=timezone.now(),
                                                                  last_update_orders=timezone.now(),
                                                                  last_update_notif=timezone.now(),
                                                                  last_update_roles=timezone.now(),
                                                                  last_update_mails=timezone.now(),))
        audits.append(ct_models.CharacterAudit.objects.create(
            character=characters[17]))

        skg1 = ct_models.EveItemGroup.objects.create(group_id=1,
                                                     name="TestGroup")
        sk1 = ct_models.EveItemType.objects.create(type_id=1,
                                                   name="Skill 1",
                                                   published=True,
                                                   group=skg1)
        sk2 = ct_models.EveItemType.objects.create(type_id=2,
                                                   name="Skill 2",
                                                   published=True,
                                                   group=skg1)
        sk3 = ct_models.EveItemType.objects.create(type_id=3,
                                                   name="Skill 3",
                                                   published=True,
                                                   group=skg1)
        sk4 = ct_models.EveItemType.objects.create(type_id=4,
                                                   name="Skill 4",
                                                   published=True,
                                                   group=skg1)
        sk5 = ct_models.EveItemType.objects.create(type_id=5,
                                                   name="Skill 5",
                                                   published=True,
                                                   group=skg1)
        skc1 = ct_models.EveItemCategory.objects.create(category_id=1,
                                                        name="TestCat")
        skg2 = ct_models.EveItemGroup.objects.create(group_id=2,
                                                     name="TestGroup",
                                                     category=skc1)
        a1 = ct_models.EveItemType.objects.create(type_id=10,
                                                  name="Asset 1",
                                                  published=True,
                                                  group=skg2)
        a2 = ct_models.EveItemType.objects.create(type_id=11,
                                                  name="Asset 2",
                                                  published=True)
        a3 = ct_models.EveItemType.objects.create(type_id=12,
                                                  name="Asset 3",
                                                  published=True)
        a4 = ct_models.EveItemType.objects.create(type_id=13,
                                                  name="Asset 4",
                                                  published=True)
        a5 = ct_models.EveItemType.objects.create(type_id=14,
                                                  name="Asset 5",
                                                  published=True)

        l1 = ct_models.EveLocation.objects.create(location_id=1,
                                                  location_name="Test Location 1",
                                                  system=s1)
        l2 = ct_models.EveLocation.objects.create(location_id=2,
                                                  location_name="Test Location 2",
                                                  system=s2)
        l3 = ct_models.EveLocation.objects.create(location_id=3,
                                                  location_name="Test Location 3",
                                                  system=s3)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=10,
                                                type_name=a1,
                                                location_name=l1,
                                                character=audits[0],
                                                blueprint_copy=False)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=10,
                                                type_name=a1,
                                                location_name=l1,
                                                character=audits[2],
                                                blueprint_copy=False)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=10,
                                                type_name=a1,
                                                location_name=l1,
                                                character=audits[15],
                                                blueprint_copy=False)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=10,
                                                type_name=a1,
                                                location_name=l1,
                                                character=audits[17],
                                                blueprint_copy=False)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=11,
                                                type_name=a2,
                                                location_name=l1,
                                                character=audits[4],
                                                blueprint_copy=False)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=11,
                                                type_name=a2,
                                                location_name=l1,
                                                character=audits[6],
                                                blueprint_copy=False)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=11,
                                                type_name=a2,
                                                location_name=l1,
                                                character=audits[15],
                                                blueprint_copy=False)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=11,
                                                type_name=a2,
                                                location_name=l1,
                                                character=audits[17],
                                                blueprint_copy=False)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=11,
                                                type_name=a2,
                                                location_name=l2,
                                                character=audits[1],
                                                blueprint_copy=False)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=11,
                                                type_name=a2,
                                                location_name=l2,
                                                character=audits[3],
                                                blueprint_copy=False)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=11,
                                                type_name=a2,
                                                location_name=l2,
                                                character=audits[14],
                                                blueprint_copy=False)

        ct_models.CharacterAsset.objects.create(item_id=0,
                                                location_flag="test",
                                                location_id=0,
                                                quantity=1,
                                                singleton=True,
                                                location_type="test",
                                                type_id=11,
                                                type_name=a2,
                                                location_name=l2,
                                                character=audits[16],
                                                blueprint_copy=False)

        ct_models.SkillList.objects.create(name="Test Skills 1",
                                           skill_list='{"Skill 1":"5"}')
        ct_models.SkillList.objects.create(name="Test Skills 2",
                                           skill_list='{"Skill 2":"1"}')

        for a in audits:
            ct_models.Skill.objects.create(character=a,
                                           skill_id=sk2.type_id,
                                           skill_name=sk2,
                                           active_skill_level=0,
                                           trained_skill_level=5,
                                           skillpoints_in_skill=500)

        ct_models.Skill.objects.create(character=audits[0],
                                       skill_id=sk1.type_id,
                                       skill_name=sk1,
                                       active_skill_level=5,
                                       trained_skill_level=5,
                                       skillpoints_in_skill=500)

        ct_models.Skill.objects.create(character=audits[9],
                                       skill_id=sk1.type_id,
                                       skill_name=sk1,
                                       active_skill_level=5,
                                       trained_skill_level=5,
                                       skillpoints_in_skill=500)

        u1 = ct_models.CharacterRoles.objects.create(
            character=audits[0], director=True, personnel_manager=True)
        u1.titles.add(cls.c1t1)

        u15 = ct_models.CharacterRoles.objects.create(
            character=audits[15], personnel_manager=True)
        u15.titles.add(cls.c2t1)

        u16 = ct_models.CharacterRoles.objects.create(
            character=audits[17], personnel_manager=True)
        u16.titles.add(cls.c2t1)

        # print("**************************")
        # print(u1.character.character.character_ownership.user.id)
        # print(u15.character.character.character_ownership.user.id)
        # print(u16.character.character.character_ownership.user.id)
        # print("**************************")

        ct_models.Skill.objects.filter(
            character=audits[0]).update(active_skill_level=5)

    def test_user_loaded_fully(self):
        _filter = ct_models.FullyLoadedFilter.objects.create(name="Fully Loaded Test",
                                                             description="Something to tell user")
        users = {}
        for user in ct_models.CharacterAudit.objects.all():
            users[user.character.character_ownership.user.id] = None

        tests = {}
        for k, u in users.items():
            tests[k] = _filter.process_filter(User.objects.get(id=k))

        self.assertTrue(tests[1])
        self.assertTrue(tests[2])
        self.assertTrue(tests[3])
        self.assertTrue(tests[4])
        self.assertTrue(tests[5])
        self.assertTrue(tests[6])
        self.assertTrue(tests[7])
        self.assertFalse(tests[8])
        self.assertFalse(tests[9])
        self.assertFalse(tests[10])

    def test_user_assets_no_loc(self):
        _filter = ct_models.AssetsFilter.objects.create(name="Assets Test",
                                                        description="Something to tell user")
        _filter.types.add(ct_models.EveItemType.objects.get(type_id=10))

        users = {}
        for user in ct_models.CharacterAudit.objects.all():
            users[user.character.character_ownership.user.id] = None

        tests = {}
        for k, u in users.items():
            tests[k] = _filter.process_filter(User.objects.get(id=k))

        self.assertTrue(tests[1])
        self.assertFalse(tests[2])
        self.assertTrue(tests[3])
        self.assertFalse(tests[4])
        self.assertFalse(tests[5])
        self.assertTrue(tests[6])
        self.assertFalse(tests[7])
        self.assertTrue(tests[8])
        self.assertFalse(tests[9])
        self.assertFalse(tests[10])

    def test_user_assets_no_loc_cat(self):
        _filter = ct_models.AssetsFilter.objects.create(name="Assets Test",
                                                        description="Something to tell user")
        _filter.categories.add(
            ct_models.EveItemCategory.objects.get(category_id=1))

        users = {}
        for user in ct_models.CharacterAudit.objects.all():
            users[user.character.character_ownership.user.id] = None

        tests = {}
        for k, u in users.items():
            tests[k] = _filter.process_filter(User.objects.get(id=k))

        self.assertTrue(tests[1])
        self.assertFalse(tests[2])
        self.assertTrue(tests[3])
        self.assertFalse(tests[4])
        self.assertFalse(tests[5])
        self.assertTrue(tests[6])
        self.assertFalse(tests[7])
        self.assertTrue(tests[8])
        self.assertFalse(tests[9])
        self.assertFalse(tests[10])

    def test_user_assets_no_loc_grp(self):
        _filter = ct_models.AssetsFilter.objects.create(name="Assets Test",
                                                        description="Something to tell user")
        _filter.groups.add(ct_models.EveItemGroup.objects.get(group_id=2))

        users = {}
        for user in ct_models.CharacterAudit.objects.all():
            users[user.character.character_ownership.user.id] = None

        tests = {}
        for k, u in users.items():
            tests[k] = _filter.process_filter(User.objects.get(id=k))

        self.assertTrue(tests[1])
        self.assertFalse(tests[2])
        self.assertTrue(tests[3])
        self.assertFalse(tests[4])
        self.assertFalse(tests[5])
        self.assertTrue(tests[6])
        self.assertFalse(tests[7])
        self.assertTrue(tests[8])
        self.assertFalse(tests[9])
        self.assertFalse(tests[10])

    def test_user_assets_loc(self):
        _filter = ct_models.AssetsFilter.objects.create(name="Assets Test",
                                                        description="Something to tell user")
        _filter.types.add(ct_models.EveItemType.objects.get(type_id=11))
        _filter.systems.add(
            ct_models.MapSystem.objects.get(name="Test System 1"))

        users = {}
        for user in ct_models.CharacterAudit.objects.all():
            users[user.character.character_ownership.user.id] = None

        tests = {}
        for k, u in users.items():
            tests[k] = _filter.process_filter(User.objects.get(id=k))

        self.assertFalse(tests[1])
        self.assertFalse(tests[2])
        self.assertFalse(tests[3])
        self.assertFalse(tests[4])
        self.assertTrue(tests[5])
        self.assertTrue(tests[6])
        self.assertTrue(tests[7])
        self.assertTrue(tests[8])
        self.assertFalse(tests[9])
        self.assertFalse(tests[10])

    def test_user_assets_loc_con(self):
        _filter = ct_models.AssetsFilter.objects.create(name="Assets Test",
                                                        description="Something to tell user")
        _filter.types.add(ct_models.EveItemType.objects.get(type_id=11))
        _filter.constellations.add(
            ct_models.MapConstellation.objects.get(name="Test Constellation 1"))

        users = {}
        for user in ct_models.CharacterAudit.objects.all():
            users[user.character.character_ownership.user.id] = None

        tests = {}
        for k, u in users.items():
            tests[k] = _filter.process_filter(User.objects.get(id=k))

        self.assertFalse(tests[1])
        self.assertFalse(tests[2])
        self.assertFalse(tests[3])
        self.assertFalse(tests[4])
        self.assertTrue(tests[5])
        self.assertTrue(tests[6])
        self.assertTrue(tests[7])
        self.assertTrue(tests[8])
        self.assertFalse(tests[9])
        self.assertFalse(tests[10])

    def test_user_assets_loc_reg(self):
        _filter = ct_models.AssetsFilter.objects.create(name="Assets Test",
                                                        description="Something to tell user")
        _filter.types.add(ct_models.EveItemType.objects.get(type_id=11))
        _filter.regions.add(
            ct_models.MapRegion.objects.get(name="Test region 1"))

        users = {}
        for user in ct_models.CharacterAudit.objects.all():
            users[user.character.character_ownership.user.id] = None

        tests = {}
        for k, u in users.items():
            tests[k] = _filter.process_filter(User.objects.get(id=k))

        self.assertFalse(tests[1])
        self.assertFalse(tests[2])
        self.assertFalse(tests[3])
        self.assertFalse(tests[4])
        self.assertTrue(tests[5])
        self.assertTrue(tests[6])
        self.assertTrue(tests[7])
        self.assertTrue(tests[8])
        self.assertFalse(tests[9])
        self.assertFalse(tests[10])

    def test_user_assets_loc_2(self):
        _filter = ct_models.AssetsFilter.objects.create(name="Assets Test",
                                                        description="Something to tell user")
        _filter.types.add(ct_models.EveItemType.objects.get(type_id=11))
        _filter.systems.add(
            ct_models.MapSystem.objects.get(name="Test System 2"))

        users = {}
        for user in ct_models.CharacterAudit.objects.all():
            users[user.character.character_ownership.user.id] = None

        tests = {}
        for k, u in users.items():
            tests[k] = _filter.process_filter(User.objects.get(id=k))

        self.assertFalse(tests[1])
        self.assertTrue(tests[2])
        self.assertFalse(tests[3])
        self.assertTrue(tests[4])
        self.assertTrue(tests[5])
        self.assertFalse(tests[6])
        self.assertTrue(tests[7])
        self.assertFalse(tests[8])
        self.assertFalse(tests[9])

    def test_user_skill_lists_alpha(self):
        _filter = ct_models.Skillfilter.objects.create(name="Skills Test",
                                                       description="Something to tell user")
        _filter.required_skill_lists.add(
            ct_models.SkillList.objects.get(name="Test Skills 2"))

        users = {}
        for user in ct_models.CharacterAudit.objects.all():
            users[user.character.character_ownership.user.id] = None

        tests = {}
        for k, u in users.items():
            tests[k] = _filter.process_filter(User.objects.get(id=k))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1])
        self.assertFalse(tests[2])
        self.assertFalse(tests[3])
        self.assertFalse(tests[4])
        self.assertFalse(tests[5])
        self.assertFalse(tests[6])
        self.assertFalse(tests[7])
        self.assertFalse(tests[8])
        self.assertFalse(tests[9])
        self.assertFalse(tests[10])

    def test_user_skill_lists_req_one(self):
        _filter = ct_models.Skillfilter.objects.create(name="Skills Test",
                                                       description="Something to tell user")
        _filter.single_req_skill_lists.add(
            ct_models.SkillList.objects.get(name="Test Skills 2"))
        _filter.required_skill_lists.add(
            ct_models.SkillList.objects.get(name="Test Skills 1"))

        users = {}
        for user in ct_models.CharacterAudit.objects.all():
            users[user.character.character_ownership.user.id] = None

        tests = {}
        for k, u in users.items():
            tests[k] = _filter.process_filter(User.objects.get(id=k))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1])
        self.assertFalse(tests[2])
        self.assertFalse(tests[3])
        self.assertFalse(tests[4])
        self.assertFalse(tests[5])
        self.assertFalse(tests[6])
        self.assertFalse(tests[7])
        self.assertFalse(tests[8])
        self.assertFalse(tests[9])
        self.assertFalse(tests[10])

    def test_user_skill_lists_audit_req_one(self):
        _filter = ct_models.Skillfilter.objects.create(name="Skills Test",
                                                       description="Something to tell user")
        _filter.single_req_skill_lists.add(
            ct_models.SkillList.objects.get(name="Test Skills 2"))
        _filter.required_skill_lists.add(
            ct_models.SkillList.objects.get(name="Test Skills 1"))

        users = []
        for user in ct_models.CharacterAudit.objects.all():
            users.append(user.character.character_ownership.user.id)

        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertFalse(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertFalse(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

        # run again and confirm cache
        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertFalse(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertFalse(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

    def test_user_skill_lists_omega(self):
        _filter = ct_models.Skillfilter.objects.create(name="Skills Test",
                                                       description="Something to tell user")
        _filter.required_skill_lists.add(
            ct_models.SkillList.objects.get(name="Test Skills 1"))

        users = {}
        for user in ct_models.CharacterAudit.objects.all():
            users[user.character.character_ownership.user.id] = None

        tests = {}
        for k, u in users.items():
            tests[k] = _filter.process_filter(User.objects.get(id=k))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1])
        self.assertFalse(tests[2])
        self.assertFalse(tests[3])
        self.assertFalse(tests[4])
        self.assertFalse(tests[5])
        self.assertFalse(tests[6])
        self.assertFalse(tests[7])
        self.assertFalse(tests[8])
        self.assertFalse(tests[9])
        self.assertTrue(tests[10])

    def test_user_skill_lists_audit_omega(self):
        _filter = ct_models.Skillfilter.objects.create(name="Skills Test",
                                                       description="Something to tell user")
        _filter.required_skill_lists.add(
            ct_models.SkillList.objects.get(name="Test Skills 1"))

        users = []
        for user in ct_models.CharacterAudit.objects.all():
            users.append(user.character.character_ownership.user.id)

        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertFalse(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertFalse(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertTrue(tests[10]['check'])

        # run again and confirm cache
        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertFalse(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertFalse(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertTrue(tests[10]['check'])

    def test_user_has_roles_director(self):
        _filter = ct_models.Rolefilter.objects.create(name="roles Test",
                                                      description="Something to tell user")
        _filter.has_director = True

        users = []
        for user in ct_models.CharacterAudit.objects.all():
            users.append(user.character.character_ownership.user.id)

        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertFalse(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertFalse(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

        # run again and confirm cache
        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertFalse(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertFalse(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

    def test_user_has_roles_personel(self):
        _filter = ct_models.Rolefilter.objects.create(name="roles Test",
                                                      description="Something to tell user")
        _filter.has_personnel_manager = True

        users = []
        for user in ct_models.CharacterAudit.objects.all():
            users.append(user.character.character_ownership.user.id)

        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertTrue(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertTrue(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

        # run again and confirm cache
        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertTrue(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertTrue(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

    def test_user_has_roles_personel_alli_filtered(self):
        _filter = ct_models.Rolefilter.objects.create(name="roles Test",
                                                      description="Something to tell user",
                                                      alliance_filter=self.alli)
        _filter.has_personnel_manager = True

        users = []
        for user in ct_models.CharacterAudit.objects.all():
            users.append(user.character.character_ownership.user.id)

        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertFalse(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertTrue(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertTrue(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

        # run again and confirm cache
        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertFalse(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertTrue(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertTrue(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

    def test_user_has_roles_personel_corp_filtered(self):
        _filter = ct_models.Rolefilter.objects.create(name="roles Test",
                                                      description="Something to tell user",
                                                      corp_filter=self.corp)
        _filter.has_personnel_manager = True

        users = []
        for user in ct_models.CharacterAudit.objects.all():
            users.append(user.character.character_ownership.user.id)

        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        print("**********")
        print(tests)
        self.assertFalse(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertTrue(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertTrue(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

        # run again and confirm cache
        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertFalse(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertTrue(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertTrue(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

    def test_user_has_title_1(self):
        _filter = ct_models.Titlefilter.objects.create(name="Title Test1",
                                                       description="Something to tell user",
                                                       titles=self.c1t1)

        users = []
        for user in ct_models.CharacterAudit.objects.all():
            users.append(user.character.character_ownership.user.id)

        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertFalse(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertFalse(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

        # run again and confirm cache
        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertTrue(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertFalse(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertFalse(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

    def test_user_has_title_1(self):
        _filter = ct_models.Titlefilter.objects.create(name="Title Test2",
                                                       description="Something to tell user",
                                                       titles=self.c2t1)

        users = []
        for user in ct_models.CharacterAudit.objects.all():
            users.append(user.character.character_ownership.user.id)

        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertFalse(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertTrue(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertTrue(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])

        # run again and confirm cache
        tests = _filter.audit_filter(User.objects.filter(id__in=users))
        # print("**********")
        # print(tests)
        self.assertFalse(tests[1]['check'])
        self.assertFalse(tests[2]['check'])
        self.assertFalse(tests[3]['check'])
        self.assertFalse(tests[4]['check'])
        self.assertFalse(tests[5]['check'])
        self.assertTrue(tests[6]['check'])
        self.assertFalse(tests[7]['check'])
        self.assertTrue(tests[8]['check'])
        self.assertFalse(tests[9]['check'])
        self.assertFalse(tests[10]['check'])
