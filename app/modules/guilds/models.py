from django.db import models
from django.contrib.auth.models import User, Group

class Guild(models.Model):
    """
    Guild model for Krypted Authentication. Guilds are used to describe a particular set of players.
    """
    # BASIC INFORMATION
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=8)
    date_formed = models.DateField(auto_now=True)
    image = models.URLField()

    # REFERENCES
    default_group = models.OneToOneField(Group, related_name="guild", on_delete=models.SET_NULL, null=True, blank=True)
    staff_group = models.OneToOneField(Group, related_name="guild_staffing", on_delete=models.SET_NULL, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name="guilds", blank=True)
    users = models.ManyToManyField(User, related_name="guilds_in", blank=True)
    users_managing = models.ManyToManyField(User, related_name="guilds_managing", blank=True)


    def __str__(self):
        return self.name

class GuildApplicationTemplate(models.Model):
    """
    Guild Application Template for Krypted Authentication
    Used to build Guild applications, which can be filled out by users and recorded as GuildApplication() objects
    """
    # REFERENCES
    guild = models.OneToOneField("Guild", on_delete=models.CASCADE, related_name="application_template")
    questions = models.ManyToManyField("GuildApplicationQuestion", blank=True)

    def __str__(self):
        return self.guild.name


class GuildApplicationQuestion(models.Model):
    """
    Guild Application Question for Krypted Authentication
    Used to be filled out by users in GuildApplication() objects, recorded as GuildApplicationResponse() objects
    """
    question_type_fields = (
        ("RESPONSE", "Response"),
        ("MODAL", "Modal")
    )
    # BASIC INFORMATION
    name = models.CharField(max_length=256)
    help_text = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=16, choices=question_type_fields)

    # OPTIONAL: MODAL
    choices = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name

class GuildApplicationResponse(models.Model):
    # BASIC INFORMATION
    response = models.TextField()
    # REFERENCES
    question = models.ForeignKey("GuildApplicationQuestion", on_delete=models.CASCADE)
    application = models.ForeignKey("GuildApplication", on_delete=models.CASCADE)

class GuildApplication(models.Model):
    application_status_fields = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected")
    )
    # BASIC INFORMATION
    status = models.CharField(max_length=16, choices=application_status_fields)

    # USER
    request_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    request_date = models.DateField(auto_now=True)

    # MANAGEMENT
    response_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications_assigned", blank=True, null=True)
    response_date = models.DateField(blank=True, null=True)

    # REFERENCES
    template = models.ForeignKey("GuildApplicationTemplate", on_delete=models.CASCADE)

    def __str__(self):
        return self.request_user.username + "'s Application to " + self.template.guild.name

    class Meta:
        permissions = (
            ('manage_guild_applications', u'Can manage Guild applications'),
            ('audit_eve_applications', u'Can audit an EVE application'),
        )
