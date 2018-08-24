from django.shortcuts import render
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView, UpdateView, FormView
from django.views.generic.detail import DetailView

from plans.models import Subscription, Plan

from .models import Profile
from .forms import SignupForm



# Create your views here.

class LoginUserView(LoginView):
	template_name="users/login.html"


class LogoutUserView(LoginRequiredMixin, LogoutView):
	next_page=reverse_lazy("profiles:login")


class SignupUserView(FormView):
	form_class=SignupForm
	template_name="users/signup.html"
	success_url=reverse_lazy("profiles:login")

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
	template_name="users/update.html"
	model=Profile
	fields=["website", "phone_number"]

	def get_object(self):
		return self.request.user.profile

	def get_success_url(self):
		useraname=self.request.user.username
		return reverse_lazy("profiles.detail", {"username": useraname})

class DetailProfileView(LoginRequiredMixin, DetailView):
	slug_field="username"
	slug_url_kwarg="username"
	queryset = User.objects.all()
	template_name="users/profile.html"
	context_object_name="user"


class MeProfileView(LoginRequiredMixin, TemplateView):
	template_name = "users/me.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["user"] = self.request.user
		context["profile"] = self.request.user.profile

		subscription_count = Subscription.objects.filter(
			profile__user__username=self.request.user.username,
			is_active=True
		).count()

		if subscription_count > 0:
			subscription = Subscription.objects.filter(
				profile__user__username=self.request.user.username,
				is_active=True
			).get()
		else:
			subscription = None

		context['subscription'] = subscription
		context['plans'] = Plan.objects.all()

		return context
	
