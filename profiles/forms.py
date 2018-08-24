from django import forms
from django.conf import settings

from django.contrib.auth.models import User

from .models import Profile

import stripe


class SignupForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        required=True
    )

    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput()
    )

    password_confirmation = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput()
    )

    first_name = forms.CharField(
        max_length=150,
        required=True
    )
    last_name = forms.CharField(
        max_length=150,
        required=True
    )

    email = forms.CharField(
        max_length=150,
        required=True
    )

    website = forms.CharField(
        max_length=150,
        required=True
    )

    phone_number = forms.CharField(
        max_length=10,
        required=True
    )

    stripe_token = forms.CharField(
        max_length=30, 
        widget=forms.HiddenInput()
    )

    def clean_username(self):
        username = self.cleaned_data["username"]

        username_exists = User.objects.filter(username=username).exists()

        if username_exists:
            raise forms.ValidationError("Username is alreade taken")

        return username

    def clean(self):
        data = super().clean()

        password = data["password"]
        password_confirmation = data["password_confirmation"]

        if password != password_confirmation:
            raise forms.ValidationError(
                "Password and Password confirmation does not match")

        return data

    def save(self):
        data = self.cleaned_data

        data.pop("password_confirmation")

        user = User.objects.create_user(
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["password"],
            email=data["email"],
        )
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_customer = stripe.Customer.create(
            source=data["stripe_token"],
            email=data["email"]
        )

        profile = Profile(
            user=user,
            website=data["website"],
            phone_number=data["phone_number"],
            stripe_user_id=stripe_customer.id
        )

        profile.save()
