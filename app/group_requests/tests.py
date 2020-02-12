from django.test import TestCase
from django.urls import reverse_lazy, reverse
from django.apps import apps
from unittest import skipIf
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import PermissionDenied
from .models import GroupRequest, OpenGroup, ClosedGroup

class GroupRequestDefaultTestCase(TestCase):
    @staticmethod
    def get_user():
        return User.objects.get(username="GroupTest")

    def setUp(self):
        if apps.is_installed('django_eveonline_group_states'):
            return 

        User.objects.create_user(username="GroupTest", 
            password="TestPassword",
            email="test@kryptedgaming.com")
        
        group_a = Group.objects.create(name="GROUP A")
        open_group = Group.objects.create(name="OPEN GROUP")
        closed_group = Group.objects.create(name="CLOSED GROUP")

        OpenGroup.objects.create(group=open_group)
        ClosedGroup.objects.create(group=closed_group)


    @skipIf(apps.is_installed('django_eveonline_group_states'), "Skipping base unit test(s) due to django_eveonline_group_states")
    def test_view_groups(self):
        url = reverse_lazy('group-list')
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test successful access
        self.client.login(username="GroupTest", password="TestPassword")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)

        expected_result = {
            "group": Group.objects.get(name="GROUP A"),
            "open": False,
            "requested": None,
            "request_count": 0,
        }
        self.assertTrue(expected_result in response.context['groups'])

        expected_result = {
            "group": Group.objects.get(name="OPEN GROUP"),
            "open": True,
            "requested": None,
            "request_count": 0,
        }
        self.assertTrue(expected_result in response.context['groups'])
    


    @skipIf(apps.is_installed('django_eveonline_group_states'), "Skipping base unit test(s) due to django_eveonline_group_states")
    def test_request_group_success(self):
        successful_group=Group.objects.get(name="GROUP A")
        url = reverse_lazy('group-request', args=(successful_group.pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test successful access
        self.client.login(username="GroupTest", password="TestPassword")
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)

        # verify group request exists
        self.assertTrue(GroupRequest.objects.filter(
            request_user=self.get_user(),
            request_group__pk=successful_group.pk,
            response_action="PENDING").exists()
            )

    @skipIf(apps.is_installed('django_eveonline_group_states'), "Skipping base unit test(s) due to django_eveonline_group_states")
    def test_request_group_success_open_group(self):
        successful_group=Group.objects.get(name="OPEN GROUP")
        url = reverse_lazy('group-request', args=(successful_group.pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test successful access
        self.client.login(username="GroupTest", password="TestPassword")
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)

        # verify group request exists
        self.assertTrue(GroupRequest.objects.filter(
            request_user=self.get_user(),
            request_group__pk=successful_group.pk,
            response_action="ACCEPTED").exists()
            )

        self.assertTrue(successful_group in self.get_user().groups.all())

    @skipIf(apps.is_installed('django_eveonline_group_states'), "Skipping base unit test(s) due to django_eveonline_group_states")
    def test_request_group_failure(self):
        unsuccessful_group=Group.objects.get(name="CLOSED GROUP")
        url = reverse_lazy('group-request', args=(unsuccessful_group.pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test successful access
        self.client.login(username="GroupTest", password="TestPassword")
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)

        # verify group request exists
        self.assertFalse(GroupRequest.objects.filter(
            request_user=self.get_user(),
            request_group__pk=unsuccessful_group.pk,
            response_action="PENDING").exists()
            )
        
        self.assertTrue(str(list(response.context['messages'])[0]) == "You do not have access to request that group.")

class GroupRequestWithGroupStatesTestCase(TestCase):
    @staticmethod
    def get_user():
        return User.objects.get(username="GroupTest")

    def setUp(self):
        if not apps.is_installed('django_eveonline_group_states'):
            return 
        from django_eveonline_group_states.models import EveGroupState, EveUserState
        group_a = Group.objects.create(name="GROUP A")
        open_group = Group.objects.create(name="OPEN GROUP")
        unknown_open_group = Group.objects.create(name="UNASSIGNED OPEN GROUP")
        closed_group = Group.objects.create(name="CLOSED GROUP")
        unknown_closed_group = Group.objects.create(name="UNASSIGNED CLOSED GROUP")

        OpenGroup.objects.create(group=open_group)
        ClosedGroup.objects.create(group=closed_group)
        OpenGroup.objects.create(group=unknown_open_group)
        ClosedGroup.objects.create(group=unknown_closed_group)

        user = User.objects.create_user(username="GroupTest", 
            password="TestPassword",
            email="test@kryptedgaming.com")

        state = EveGroupState.objects.create(
            name="Default",
            priority=-1,
        )
        state.default_groups.add(group_a)
        state.enabling_groups.add(open_group)
        state.enabling_groups.add(closed_group)

        EveUserState(
            user=user, 
            state=state
        ).save()

    @skipIf(not apps.is_installed('django_eveonline_group_states'), "Skipping specialized test(s) due to django_eveonline_group_states")
    def test_view_groups_with_group_states(self):
        url = reverse_lazy('group-list')
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test successful access
        self.client.login(username="GroupTest", password="TestPassword")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)

        expected_result = {
            "group": Group.objects.get(name="GROUP A"),
            "open": False,
        }
        self.assertTrue(expected_result in response.context['groups'])

        expected_result = {
            "group": Group.objects.get(name="OPEN GROUP"),
            "open": True,
        }
        self.assertTrue(expected_result in response.context['groups'])

        expected_result = {
            "group": Group.objects.get(name="UNASSIGNED OPEN GROUP"),
            "open": True,
        }

        self.assertTrue(expected_result not in response.context['groups'])

        expected_result = {
            "group": Group.objects.get(name="CLOSED GROUP"),
            "open": True,
        }

        self.assertTrue(expected_result not in response.context['groups'])

    @skipIf(not apps.is_installed('django_eveonline_group_states'), "Skipping specialized test(s) due to django_eveonline_group_states")
    def test_request_group_with_group_states(self):
        successful_group=Group.objects.get(name="GROUP A")
        url = reverse_lazy('group-request', args=(successful_group.pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test successful access
        self.client.login(username="GroupTest", password="TestPassword")
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)

        # verify group request exists
        self.assertTrue(GroupRequest.objects.filter(
            request_user=self.get_user(),
            request_group__pk=successful_group.pk,
            response_action="PENDING").exists()
            )

    @skipIf(not apps.is_installed('django_eveonline_group_states'), "Skipping specialized test(s) due to django_eveonline_group_states")
    def test_request_group_with_group_states_open_group(self):
        successful_group=Group.objects.get(name="OPEN GROUP")
        url = reverse_lazy('group-request', args=(successful_group.pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test successful access
        self.client.login(username="GroupTest", password="TestPassword")
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)

        # verify group request exists
        self.assertTrue(GroupRequest.objects.filter(
            request_user=self.get_user(),
            request_group__pk=successful_group.pk,
            response_action="ACCEPTED").exists()
            )

        self.assertTrue(successful_group in self.get_user().groups.all())

    @skipIf(not apps.is_installed('django_eveonline_group_states'), "Skipping base unit test(s) due to django_eveonline_group_states")
    def test_request_group_with_group_states_open_group_not_in_state(self):
        unsuccessful_group=Group.objects.get(name="UNASSIGNED OPEN GROUP")
        url = reverse_lazy('group-request', args=(unsuccessful_group.pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test successful access
        self.client.login(username="GroupTest", password="TestPassword")
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)

        # verify group request exists
        self.assertFalse(GroupRequest.objects.filter(
            request_user=self.get_user(),
            request_group__pk=unsuccessful_group.pk,
            response_action="PENDING").exists()
            )
        
        self.assertTrue(str(list(response.context['messages'])[0]) == "You do not have access to request that group.")

    
class GroupRequestAdministrationTestCase(TestCase):
    @staticmethod
    def get_user():
        return User.objects.get(username="GroupTest")

    def setUp(self):
        group = Group.objects.create(name="GROUP")
        admin = User.objects.create_user(username="GroupAdmin", 
            password="TestPassword",
            email="test@kryptedgaming.com",
            )
        manager = User.objects.create_user(username="GroupManager", 
            password="TestPassword",
            email="test@kryptedgaming.com")

        Permission.objects.get(codename="view_grouprequest").user_set.add(manager)
        Permission.objects.get(codename="change_grouprequest").user_set.add(manager)
        Permission.objects.get(codename="view_grouprequest").user_set.add(admin)
        Permission.objects.get(codename="change_grouprequest").user_set.add(admin)
        Permission.objects.get(codename="bypass_group_requirement").user_set.add(admin)

        user_1 = User.objects.create_user(username="User1", 
            password="TestPassword",
            email="test@kryptedgaming.com")
        user_2 = User.objects.create_user(username="User2", 
            password="TestPassword",
            email="test@kryptedgaming.com")

        GroupRequest(
            request_user=user_1,
            request_group=group,
        ).save()

        GroupRequest(
            request_user=user_2,
            request_group=group,
        ).save()

    def test_view_group_request_as_admin(self):
        user = User.objects.get(username="GroupAdmin")
        group_pk = Group.objects.get(name="GROUP").pk
        # test redirect
        url = reverse_lazy('group-request-list', args=(group_pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test successful access
        self.client.login(username="GroupAdmin", password="TestPassword")
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context['group_requests'].count() == 2)

    def test_view_group_request_as_manager(self):
        user = User.objects.get(username="GroupManager")
        group = Group.objects.get(name="GROUP")
        # test redirect
        url = reverse_lazy('group-request-list', args=(group.pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test rejected access
        self.client.login(username="GroupManager", password="TestPassword")
        response = self.client.get(url)
        self.assertTrue(response.status_code != 200)
        user.groups.add(group)
        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context['group_requests'].count() == 2)
        user.groups.remove(group)

    def test_approve_group_request_as_admin(self):
        user = User.objects.get(username="GroupAdmin")
        group_pk = Group.objects.get(name="GROUP").pk
        group_request_pk = GroupRequest.objects.all()[0].pk
        # test redirect
        url = reverse_lazy('group-request-approve', args=(group_pk, group_request_pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test successful access
        self.client.login(username="GroupAdmin", password="TestPassword")
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)
        gr = GroupRequest.objects.get(pk=1)
        self.assertTrue(gr.response_action == "ACCEPTED")
        self.assertTrue(gr.request_group in gr.request_user.groups.all())
    
    def test_deny_group_request_as_admin(self):
        user = User.objects.get(username="GroupAdmin")
        group_pk = Group.objects.get(name="GROUP").pk
        group_request_pk = GroupRequest.objects.all()[0].pk
        # test redirect
        url = reverse_lazy('group-request-deny', args=(group_pk, group_request_pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test successful access
        self.client.login(username="GroupAdmin", password="TestPassword")
        response = self.client.get(url, follow=True)
        gr = GroupRequest.objects.get(pk=1)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(gr.response_action == "REJECTED")
        self.assertTrue(gr.request_group not in gr.request_user.groups.all())

    def test_approve_group_request_as_manager(self):
        user = User.objects.get(username="GroupManager")
        group = Group.objects.get(name="GROUP")
        group_request_pk = GroupRequest.objects.all()[0].pk
        # test redirect
        url = reverse_lazy('group-request-approve', args=(group.pk, group_request_pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test fail
        self.client.login(username="GroupManager", password="TestPassword")
        response = self.client.get(url)
        gr = GroupRequest.objects.get(pk=1)
        self.assertTrue(gr.response_action != "ACCEPTED")
        self.assertTrue(gr.request_group not in gr.request_user.groups.all())

        # test success
        user.groups.add(group)
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)
        gr = GroupRequest.objects.get(pk=1)
        self.assertTrue(gr.response_action == "ACCEPTED")
        self.assertTrue(gr.request_group in gr.request_user.groups.all())

    def test_deny_group_request_as_manager(self):
        user = User.objects.get(username="GroupManager")
        group = Group.objects.get(name="GROUP")
        group_request_pk = GroupRequest.objects.all()[0].pk
        # test redirect
        url = reverse_lazy('group-request-deny', args=(group.pk, group_request_pk,))
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)

        # test fail
        self.client.login(username="GroupManager", password="TestPassword")
        response = self.client.get(url)
        gr = GroupRequest.objects.get(pk=1)
        self.assertTrue(gr.response_action != "REJECTED")
        
        # test success
        user.groups.add(group)
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)
        gr = GroupRequest.objects.get(pk=1)
        self.assertTrue(gr.response_action == "REJECTED")
        self.assertTrue(gr.request_group not in gr.request_user.groups.all())
    
        


