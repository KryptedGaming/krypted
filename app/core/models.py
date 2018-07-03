from django.db import models
from django.contrib.auth.models import User, Group


class Game(models.Model):
    title = models.CharField(max_length=24, unique=True)
    leadership = models.ManyToManyField(User)
    def __str__(self):
        return self.title
    def is_guild(self):
        if Guild.objects.filter(pk=self.pk).count() > 0:
            return True
        else:
            return False

class Guild(Game):
    image = models.URLField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.CharField(max_length=24, blank=True, null=True)

    def __str__(self):
        return self.title

class Notification(models.Model):
    title = models.CharField(max_length=24)
    message = models.CharField(max_length=500)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def mark_read(self):
        try:
            read = True
            return True
        except:
            pass
    def notify_user(self, user):
        try:
            self.title = "System"
            self.user = user
            self.save()
        except:
            pass

class Profile(models.Model):
    timezone_choices = (
        ("EU", "EU"),
        ("US", "US"),
        ("AU", "AU")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Profile Information
    biography = models.CharField(max_length=1500, blank=True, null=True)
    timezone = models.CharField(choices=timezone_choices, max_length=2, blank=True, null=True)
    active = models.BooleanField(default=True)

    # Community Information
    points = models.IntegerField(default=0)
    games = models.ManyToManyField('Game', related_name='games')
    guilds = models.ManyToManyField('Guild', related_name='guilds')

    # Social
    twitter = models.URLField(max_length=32, blank=True, null=True)
    steam = models.URLField(max_length=255, blank=True, null=True)
    blizzard = models.CharField(max_length=32, blank=True, null=True)
    discord = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Event(models.Model):
    importance_choices = (
            ("1", "Low"),
            ("2", "Medium"),
            ("3", "High")
            )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now=True)
    date_occuring = models.DateTimeField(auto_now=False)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=128, blank=True, null=True)
    notes = models.CharField(max_length=32, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    importance = models.CharField(choices=importance_choices, max_length=12, blank=True, null=True)

class GroupRequest(models.Model):
    status_choices = (
            ("Pending", "Pending"),
            ("Accepted", "Accepted"),
            ("Rejected", "Rejected"),
            ("Vetoed", "Vetoed")
            )
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=32, choices=status_choices)
    date_requested = models.DateField(auto_now=True)
    date_updated = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    processed_by = models.ForeignKey(User, related_name='processor', on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey("GroupEntity", on_delete=models.CASCADE)

    class Meta:
        permissions = (
                ('manage_group_requests', u'Can manage group requests.'),
                ('audit_group_requests', u'Can view the group request audit log.')
        )

class GroupEntity(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    description = models.CharField(max_length=512, blank=True)
    hidden = models.BooleanField(default=True, help_text="Hidden from the apply menu.")
    public = models.BooleanField(default=False, help_text="Automatically join upon request.")
    managers = models.ManyToManyField(User, blank=True, help_text="Users who can accept/decline requests.")
