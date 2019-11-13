import django
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import PermissionDenied
from .models import ApplicationTemplate, ApplicationQuestion, Application, ApplicationResponse

class ApplicationClientTestCase(TestCase):
    @staticmethod
    def get_user():
        return User.objects.get(username="TestUser")

    def setUp(self):
        User.objects.create_user(username="TestUser", 
            password="TestPassword",
            email="test@kryptedgaming.com")

        ApplicationQuestion(
            name="Question 1: How old are you?",
            help_text="Provide a number.",
            type="RESPONSE"
        ).save()

        ApplicationQuestion(
            name="Question 2: What is your name?",
            help_text="Provide a number.",
            type="RESPONSE"
        ).save()

        template_1 = ApplicationTemplate.objects.create(
            name="Template 1",
        )

        template_2 = ApplicationTemplate.objects.create(
            name="Template 2",
        )

        template_3 = ApplicationTemplate.objects.create(
            name="Template 3",
            required_group=Group.objects.create(name="TEST"),
        )

        for question in ApplicationQuestion.objects.all():
            template_1.questions.add(question)
            template_2.questions.add(question)

        template_1.groups_to_add.add(Group.objects.create(name="GROUP-TO-ADD"))
        template_1.groups_to_remove.add(Group.objects.create(name="GROUP-TO-REMOVE"))

        application_1 = Application.objects.create(
            status="PENDING",
            request_user=self.get_user(),
            template=template_1,
        )
        for question in application_1.template.questions.all():
            ApplicationResponse(
                response="LOREM IPSUM",
                question=question,
                application=application_1
            ).save()

        Application(
            status="PENDING",
            request_user=self.get_user(),
            template=template_2,
        ).save()

        Application(
            status="PENDING",
            request_user=User.objects.create_user(username="Test", 
                password="TestUser", 
                email="test@test.com"),
            template=template_2
        ).save()

    def test_unique_together(self):
        application = Application(
            status="PENDING",
            request_user=self.get_user(),
            template=ApplicationTemplate.objects.all()[0],
        )
        with self.assertRaises(Exception) as raised:
            application.save()
        self.assertEqual(django.db.utils.IntegrityError, type(raised.exception)) 

    def test_view_applications(self):
        # test login redirect
        url = reverse_lazy('application-list')
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test login - permission denied
        self.client.login(username="TestUser", password="TestPassword")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test successful access
        Permission.objects.get(codename="view_application").user_set.add(self.get_user())
        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)
        Permission.objects.get(codename="view_application").user_set.clear()
        # verify context
        self.assertTrue(response.context['applications'].count() == 3)

    def test_my_applications(self):
        # test login redirect
        url = reverse_lazy('my-applications')
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test succesful access
        self.client.login(username="TestUser", password="TestPassword")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)
        # test context
        self.assertTrue(response.context['user_applications'].count() == 2)
        self.assertTrue(response.context['application_templates'].count() == 2)
        # test with new group as hidden template discovery
        self.get_user().groups.add(Group.objects.get(name="TEST"))
        response = self.client.get(url)
        self.assertTrue(response.context['application_templates'].count() == 3)
        self.get_user().groups.remove(Group.objects.get(name="TEST"))
        self.assertTrue(response.context['application_templates'].count() == 2)
        # test with existing application as hidden template discovery
        Application.objects.create(
            status="PENDING",
            template=ApplicationTemplate.objects.get(name="Template 3"),
            request_user=self.get_user(),
        )
        response = self.client.get(url)
        self.assertTrue(response.context['application_templates'].count() == 3)

    def test_view_application(self):
        url = reverse('application-detail', args=(1,))
        # test login redirect
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test login - permission denied
        self.client.login(username="TestUser", password="TestPassword")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test success
        Permission.objects.get(codename="view_application").user_set.add(self.get_user())
        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)
        Permission.objects.get(codename="view_application").user_set.clear()
        # verify context
        self.assertTrue(response.context['application'].pk == 1)
        self.assertTrue(response.context['responses'].count() == 2)

    def test_create_application(self):
        url = reverse('application-create', args=(1,))
        # test login redirect
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test get form 
        self.client.login(username="TestUser", password="TestPassword")
        response = self.client.get(url)
        self.assertTrue(response.context['template'].pk == 1)
        # test success
        Application.objects.get(template__id=1).delete()
        application_form = {
            response.context['template'].questions.all()[0].pk: "Hello World!",
            response.context['template'].questions.all()[1].pk: "It's me!",
        }
        response = self.client.post(url, application_form)
        created_application = Application.objects.get(template__id=1)
        self.assertTrue(created_application.applicationresponse_set.all()[0].response == "Hello World!")
        self.assertTrue(created_application.applicationresponse_set.all()[1].response == "It's me!")

    def test_approve_application(self):
        application = Application.objects.get(template__name="Template 1")
        url = reverse('application-approve', args=(application.pk,))
        self.get_user().groups.add(application.template.groups_to_remove.all()[0])
        # test login redirect
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test login - permission denied
        self.client.login(username="TestUser", password="TestPassword")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test success
        Permission.objects.get(codename="change_application").user_set.add(self.get_user())
        response = self.client.get(url,follow=True)
        self.assertTrue(response.status_code == 200)
        application = Application.objects.get(template__name="Template 1")
        self.assertTrue(application.status == "ACCEPTED")
        for group in application.template.groups_to_add.all():
            self.assertTrue(group in self.get_user().groups.all())
        for group in application.template.groups_to_remove.all():
            self.assertTrue(group not in self.get_user().groups.all())
        Permission.objects.get(codename="change_application").user_set.clear()

    def test_deny_application(self):
        application = Application.objects.get(template__name="Template 1")
        url = reverse('application-deny', args=(application.pk,))
        self.get_user().groups.add(application.template.groups_to_add.all()[0])
        self.get_user().groups.add(application.template.groups_to_remove.all()[0])
        # test login redirect
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test login - permission denied
        self.client.login(username="TestUser", password="TestPassword")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test success
        Permission.objects.get(codename="change_application").user_set.add(self.get_user())
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)
        application = Application.objects.get(template__name="Template 1")
        self.assertTrue(application.status == "REJECTED")
        for group in application.template.groups_to_add.all():
            self.assertTrue(group not in self.get_user().groups.all())
        for group in application.template.groups_to_remove.all():
            self.assertTrue(group not in self.get_user().groups.all())
        Permission.objects.get(codename="change_application").user_set.clear()

    def test_assign_application(self):
        application = Application.objects.get(template__name="Template 1")
        url = reverse('application-assign', args=(application.pk,))
        # test login redirect
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test login - permission denied
        self.client.login(username="TestUser", password="TestPassword")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        # test success
        Permission.objects.get(codename="change_application").user_set.add(self.get_user())
        response = self.client.get(url, follow=True)
        self.assertTrue(response.status_code == 200)
        application = Application.objects.get(template__name="Template 1")
        self.assertTrue(application.response_user == application.request_user)













        
        
        