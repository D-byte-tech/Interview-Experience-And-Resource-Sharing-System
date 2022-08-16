from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.

class TestUser(models.Model):
    userid = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()

def __str__(self):
        return self.first_name


class InterviewDatabase(models.Model):
   
    interviewID = models.BigAutoField(primary_key=True)
    date = models.DateField()
    year = models.IntegerField()
    cname = models.CharField(max_length=30)
    branch = models.CharField(max_length=30)
    Userid = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    title = models.TextField()
    interexp = models.TextField()
    file= models.FileField(upload_to='interview/interviewPdf', null = True, blank = True)

    def __str__(self):
        return self.cname


class ResourceDatabase(models.Model):

    resourceID = models.BigAutoField(primary_key=True)
    date = models.DateField()
    sname = models.CharField(max_length=30)
    Userid = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    topic = models.TextField()
    resourceDesc = models.TextField(null = True, blank = True)
    file= models.FileField(upload_to='resource/resourcePdf')

    def __str__(self):
        return self.sname





class Profile(models.Model):
    user = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
    role = models.CharField(max_length=15)
    branch = models.CharField(max_length=30)
    company_name = models.CharField(max_length=30, null=True)
    yoj = models.IntegerField(null=True)
    linkedIn = models.URLField(max_length=100)
    forget_pwd_token = models.CharField(max_length=100, default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile,sender=User)



