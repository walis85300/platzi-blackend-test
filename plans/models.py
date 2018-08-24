from django.db import models
from profiles.models import Profile

# Create your models here.


class Plan(models.Model):
    description = models.CharField(max_length=120, null=False)
    price = models.DecimalField(
                                max_digits=5,
                                decimal_places=2,
                                null=False)

    is_annual = models.BooleanField(default=False)

    stripe_plan_id = models.CharField(max_length=50, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    stripe_subscription_id = models.CharField(max_length=20)
    ends_at = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    canceled_at = models.DateTimeField(null=True)
