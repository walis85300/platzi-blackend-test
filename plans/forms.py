from django import forms

from .models import Subscription


class CancelSubscriptionForm(forms.Form):

    subscription_id = forms.CharField(
        max_length=20,
        required=True)


class CreateSubscriptionForm(forms.Form):
	
    plan_id = forms.CharField(
        max_length=20,
        required=True)
