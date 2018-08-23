from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	website = models.CharField(max_length=150, null=True)
	phone_number = models.CharField(max_length=10, null=True)


	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username
	

