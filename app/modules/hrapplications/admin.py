from django.contrib import admin
from modules.hrapplications.models import ApplicationTemplate, Application, Question, Comment, Response

# Register your models here.
@admin.register(ApplicationTemplate)
class ApplicationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'guild')

    def guild(self, applicationtemplate):
        return applicationtemplate.guild.name

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'guild')

    def user(self, application):
        return application.user

    def guild(self, application):
        return application.template.guild.title

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'help_text')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'response')

    def user(self, response):
        return response.application.user

    def question(self, response):
        return response.question

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('application', 'text', 'creator')

    def application(self, comment):
        return application.template.name

    def creator(self, comment):
        return creator
