from django.contrib.auth.models import UserManager, AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
import pytz

ist_timezone = pytz.timezone('Asia/Kolkata')
current_datetime = timezone.now().astimezone(ist_timezone)

# Format the datetime using strftime with a custom format string
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
# Create your models here.
class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=False, unique=True, max_length=30)
    password = models.CharField(null=False, max_length=20)
    first_name = models.CharField(null=False, max_length=20)
    last_name = models.CharField(null=False, max_length=10)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.TextField(null=True)
    posted_date = models.DateTimeField(null=False, default=formatted_datetime)
    blog = models.TextField(null=False, max_length=1024)
    is_active = models.BooleanField(default=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=False)
    comment = models.TextField()
    is_liked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_comment = models.BooleanField(default=False)
    # Timestamp
    # User as Foreign Key
    # Blog Place as textbox
    # Isactive for updating and deleting the post
    # Likes
