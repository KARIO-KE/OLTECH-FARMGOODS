from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class CustomUser(AbstractUser):
    # here you can add any custom field if necessary
    bio = models.TextField(null=True, blank=True)
    test = models.TextField(null=True, blank=True)
    is_buyer = models.BooleanField(default=False)
    is_farmer = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    short_message = models.CharField(max_length=255, blank=True, null=True)
    full_message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

    def __str__(self):
        return self.username

    '''
     null 
       definition : the column will store records as NULL if no input is given
       usage : applies to the database layer 
       default: False
     blank 
       definition : if you want to allow empty values when submitting the form 
       usage : if you want to allow empty values when submitting the form 

    '''


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Farmer(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField()  # URL to the farmer's image
    short_message = models.TextField()
    full_message = models.TextField()

    def __str__(self):
        return self.name
