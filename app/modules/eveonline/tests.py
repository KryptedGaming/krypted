from django.test import TestCase
from django.contrib.auth.models import User, Group
from modules.eveonline.models import EveGroupIntegration, EveCharacter, EveCorporation

# Create your tests here.
class EveGroupIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@test.com", "test")
        self.group = Group.objects.create(name="test")
        self.primary_eve_corporation = EveCorporation.objects.create(
            name="PRIMARY_TEST_CORP",
            ticker="TEST",
            member_count=0,
            alliance_id=0,
            tax_rate=0,
            primary_entity=True,
            corporation_id=1,
        )
        self.secondary_eve_corporation = EveCorporation.objects.create(
            name="TEST2",
            ticker="TEST2",
            member_count=0,
            alliance_id=0,
            tax_rate=0,
            blue_entity=True,
            corporation_id=2,
        )
        self.random_eve_corporation = EveCorporation.objects.create(
            name="TEST3",
            ticker="TEST3",
            member_count=0,
            alliance_id=0,
            tax_rate=0,
            corporation_id=3,
        )
        self.main_eve_character = EveCharacter.objects.create(
            user=self.user,
            character_alt_type=None,
            main=None,
            character_name="main_eve_character_test",
            character_id=1,
            corporation=self.random_eve_corporation
            )
        self.second_eve_character = EveCharacter.objects.create(
            user=self.user,
            character_alt_type="super_alt",
            main=self.main_eve_character,
            character_name="second_eve_character_test",
            character_id=2,
            corporation=self.random_eve_corporation
            )
        self.eve_integration = EveGroupIntegration.objects.create(group=self.group)

    def test_primary_status(self):
        # set to primary status
        self.eve_integration.status = "PRIMARY"
        self.eve_integration.corporations.clear()
        self.eve_integration.character_alt_type = None 
        self.eve_integration.save()
        # test failure 
        self.main_eve_character.corporation = self.random_eve_corporation
        self.main_eve_character.save()
        self.assertIs(self.eve_integration.audit_user(self.user), False)
        self.assertIs 
        # test success
        self.main_eve_character.corporation = self.primary_eve_corporation
        self.main_eve_character.save()
        self.assertIs(self.eve_integration.audit_user(self.user), True)

    def test_blue_status(self):
        # set to blue status
        self.eve_integration.status = "BLUE"
        self.eve_integration.corporations.clear()
        self.eve_integration.character_alt_type = None 
        self.eve_integration.save()
        # test failure 
        self.main_eve_character.corporation = self.random_eve_corporation
        self.main_eve_character.save()
        self.assertIs(self.eve_integration.audit_user(self.user), False)
        self.assertIs 
        # test success
        self.main_eve_character.corporation = self.secondary_eve_corporation
        self.main_eve_character.save()
        self.assertIs(self.eve_integration.audit_user(self.user), True)
        # reset
        self.main_eve_character.corporation = self.random_eve_corporation
    
    def test_corporation(self):
        # setup 
        self.eve_integration.status = None 
        self.eve_integration.corporations.add(self.primary_eve_corporation)
        self.eve_integration.character_alt_type = None 
        self.eve_integration.save()
        # test failure 
        self.assertIs(self.eve_integration.audit_user(self.user), False)
        # test success
        self.second_eve_character.corporation = self.primary_eve_corporation
        self.second_eve_character.save()
        self.assertIs(self.eve_integration.audit_user(self.user), True)
        # reset 
        self.main_eve_character.corporation = self.random_eve_corporation
        self.second_eve_character = self.random_eve_corporation
        self.main_eve_character.save()
        self.second_eve_character.save()
    
    def test_alt_type(self):
        # setup 
        self.eve_integration.status = "PRIMARY"
        self.eve_integration.corporations.clear()
        self.eve_integration.character_alt_type = "super_alt"
        self.eve_integration.save()
        # test failure 
        self.second_eve_character.corporation = self.random_eve_corporation
        self.second_eve_character.save()
        self.assertIs(self.eve_integration.audit_user(self.user), False)
        # test success 
        self.second_eve_character.corporation = self.primary_eve_corporation
        self.second_eve_character.save()
        self.assertIs(self.eve_integration.audit_user(self.user), True)