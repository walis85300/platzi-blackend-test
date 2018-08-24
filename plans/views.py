from datetime import datetime

import os
import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView

from .forms import CancelSubscriptionForm, CreateSubscriptionForm
from .models import Subscription, Plan


# Create your views here.

class CancelSubscriptionView(LoginRequiredMixin, FormView):
    success_url = reverse_lazy("profiles:me_profile")
    form_class = CancelSubscriptionForm

    def form_valid(self, form):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        stripe_subscription_id = form.cleaned_data.get('subscription_id')
        subscription_stripe = stripe.Subscription.retrieve(
            stripe_subscription_id)

        subscription_stripe.delete()

        subscription = Subscription.objects.get(
            stripe_subscription_id=stripe_subscription_id)

        subscription.is_active = False
        subscription.canceled_at = timezone.now()
        subscription.save()

        messages.success(self.request, 'Subscription has been canceled')

        return super().form_valid(form)


class CreateSubscriptionView(LoginRequiredMixin, FormView):
    form_class = CreateSubscriptionForm
    success_url = reverse_lazy("profiles:me_profile")

    def form_valid(self, form):

        stripe.api_key = settings.STRIPE_SECRET_KEY
        plan_id = form.cleaned_data.get('plan_id')

        subscription_stripe = stripe.Subscription.create(
            customer=self.request.user.profile.stripe_user_id,
            items=[
                {
                    "plan": plan_id,
                },
            ]
        )
        ends_at = subscription_stripe.current_period_end

        subscription = Subscription(
            plan=Plan.objects.get(stripe_plan_id=plan_id),
            profile=self.request.user.profile,
            ends_at=ends_at,
            stripe_subscription_id=subscription_stripe.id)

        subscription.save()

        messages.success(self.request, 'You are subscribed now, wait for email')

        return super().form_valid(form)
