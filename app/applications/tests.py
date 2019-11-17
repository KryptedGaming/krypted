import django
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import PermissionDenied
from .models import ApplicationTemplate, ApplicationQuestion, Application, ApplicationResponse
import uuid

class ApplicationClientTestCase(TestCase):
    @staticmethod
    def create_user():
        return User.objects.create_user(username=str(uuid.uuid4()), password="password")

    @staticmethod
    def create_template(template_name):
        template = ApplicationTemplate.objects.create(name=template_name, required_group=None)
        for question in ApplicationQuestion.objects.all():
            template.questions.add(question)
        return template 

    @staticmethod
    def create_application(template, user):
        application = Application.objects.create(
            template=template,
            request_user=user, 
        )
        for question in application.template.questions.all():
            ApplicationResponse(
                response="LOREM IPSUM",
                question=question,
                application=application
            ).save()
        return application
    
    def verify_login_redirect(self, url):
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
    
    def verify_permission_required_and_return_success(self, url, user, permission, code=200):
        self.client.login(username=user.username, password="password")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 302)
        Permission.objects.get(codename=permission).user_set.add(user)
        response = self.client.get(url)
        self.assertTrue(response.status_code == code)
        Permission.objects.get(codename=permission).user_set.clear()
        return response 

    def get_success(self, url, user):
        self.client.login(username=user.username, password="password")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)
        return response

    def setUp(self):
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

    def test_unique_together(self):
        template = self.create_template("test_unique_together")
        user = self.create_user()
        self.create_application(template=template, user=user)
        # attempt to duplicate
        application = Application(
            status="PENDING",
            request_user=user,
            template=template,
        )
        with self.assertRaises(Exception) as raised:
            application.save()
        self.assertEqual(django.db.utils.IntegrityError, type(raised.exception)) 

    def test_view_applications(self):
        url = reverse_lazy('application-list')
        user = self.create_user()
        template = self.create_template('test_view_applications')
        self.create_application(template, user)
        self.verify_login_redirect(url)
        response = self.verify_permission_required_and_return_success(url, user, 'view_application')
        
        self.assertTrue(response.context['applications'].count() >= 1)

    def test_my_applications(self):
        url = reverse_lazy('my-applications')
        user = self.create_user()
        template_a = self.create_template('test_my_applications_a')
        # template w/ app
        template_b = self.create_template('test_my_applications_b')
        application_b = self.create_application(template=template_b, user=user)
        # hidden template
        template_c = self.create_template('test_my_applications_b')
        group_c = Group.objects.create(name="test_my_applications_c")
        template_c.required_group = group_c 
        template_c.save() 
        # grandfathered template (existing application)
        template_d = self.create_template('test_my_applications_d')
        application_d = self.create_application(template=template_d, user=user)
        
        self.verify_login_redirect(url)
        response = self.get_success(url, user)

        # test context
        self.assertTrue([application_b, application_d] == list(response.context['user_applications']))
        expected_result = [
            {"template": template_a, "in_progress": False, "application": None},
            {"template": template_b, "in_progress": True, "application": application_b},
            {"template": template_d, "in_progress": True, "application": application_d}
        ]
        self.assertTrue(expected_result == response.context['application_templates'])

    def test_view_application(self):
        Application.objects.all().delete()
        ApplicationTemplate.objects.all().delete()
        user = self.create_user()
        template = self.create_template('test_view_application')
        application = self.create_application(template=template, user=user)

        url = reverse('application-detail', args=(application.pk,))
        
        self.verify_login_redirect(url)
        response = self.verify_permission_required_and_return_success(url, user, 'view_application')
        
        # verify context
        self.assertTrue(response.context['application'].pk == application.pk)
        self.assertTrue(response.context['responses'].count() == 2)

    def test_create_application(self):
        template = self.create_template('test_view_application')
        user = self.create_user()
        url = reverse('application-create', args=(template.pk,))
        self.verify_login_redirect(url)
        response = self.get_success(url, user)
        self.assertTrue(response.context['template'] == template)
        # test success
        application_form = {
            "question_%s" % response.context['template'].questions.all()[0].pk: "Hello World!",
            "question_%s" % response.context['template'].questions.all()[1].pk: "It's me!",
        }
        response = self.client.post(url, application_form)
        created_application = Application.objects.get(template=template)
        self.assertTrue(created_application.applicationresponse_set.all()[0].response == "Hello World!")
        self.assertTrue(created_application.applicationresponse_set.all()[1].response == "It's me!")

    def test_approve_application(self):
        user = self.create_user()
        template = self.create_template('test_approve_application')
        application = self.create_application(template=template, user=user)
        template.groups_to_add.add(Group.objects.create(name="test_approve_application_add"))
        template.groups_to_remove.add(Group.objects.create(name="test_approve_application_remove"))
        user.groups.add(Group.objects.get(name="test_approve_application_remove"))
        url = reverse('application-approve', args=(application.pk,))

        self.verify_login_redirect(url)
        self.verify_permission_required_and_return_success(url, user, 'change_application', 302)

        application = Application.objects.get(template__name="test_approve_application")
        user = User.objects.get(pk=user.pk) # refresh 
        self.assertTrue(application.status == "ACCEPTED")
        for group in application.template.groups_to_add.all():
            self.assertTrue(group in user.groups.all())
        for group in application.template.groups_to_remove.all():
            self.assertTrue(group not in user.groups.all())

    def test_deny_application(self):
        user = self.create_user()
        template = self.create_template('test_deny_application')
        application = self.create_application(template=template, user=user)
        template.groups_to_add.add(Group.objects.create(name="test_deny_application_add"))
        template.groups_to_remove.add(Group.objects.create(name="test_deny_application_remove"))
        user.groups.add(Group.objects.get(name="test_deny_application_remove"))
        url = reverse('application-deny', args=(application.pk,))

        self.verify_login_redirect(url)
        self.verify_permission_required_and_return_success(url, user, 'change_application', 302)

        application = Application.objects.get(template__name="test_deny_application")
        user = User.objects.get(pk=user.pk) # refresh 
        self.assertTrue(application.status == "REJECTED")
        for group in application.template.groups_to_add.all():
            self.assertTrue(group not in user.groups.all())
        for group in application.template.groups_to_remove.all():
            self.assertTrue(group not in user.groups.all())












        
        
        