from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. User Profile for Roles
class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',null=True,blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# 2. Classroom Model
class Classroom(models.Model):
    name = models.CharField(max_length=50) # e.g., Class 10A
    section = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return f"{self.name} {self.section}"

# 3. Subject Model
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return self.name

# 4. Teacher Model (Linked to Profile)
class Teacher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,null=True,blank=True)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.profile.user.get_full_name() or self.profile.user.username

# 5. Timetable Entry
class TimetableEntry(models.Model):
    DAYS = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE,null=True,blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True,blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True,blank=True)
    day = models.CharField(max_length=10, choices=DAYS)
    period = models.IntegerField(null=True,blank=True) # 1, 2, 3...

    class Meta:
        unique_together = ('classroom', 'day', 'period')

    def __str__(self):
        return f"{self.classroom} - {self.day} P{self.period}"

# --- SIGNALS: THIS PREVENTS THE "USER HAS NO PROFILE" ERROR ---

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile whenever a new User is created."""
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Ensure the profile is saved whenever the User is updated."""
    if hasattr(instance, 'profile'):
        instance.profile.save()