from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


from plans.models import Subscription

from datetime import datetime
import json

# Create your views here.


@require_http_methods(["POST"])
@csrf_exempt
def webhook_dispatcher(request):

	event_json = json.load(request)

	event_name = event_json["type"].replace(".", "_")

	if event_name in dispatch:
		dispatch[event_name](event_json["data"]["object"])
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=404)


def customer_subscription_created(request):
	subscription = Subscription.objects.get(
		stripe_subscription_id=request["id"]
	)

	if request["status"] == "active":
		ends_at = datetime.utcfromtimestamp(
			int(request["current_period_end"])).strftime('%Y-%m-%d %H:%M:%S')

		subscription.is_active = True
		subscription.ends_at = ends_at
		subscription.save()

		send_mail(
			"Subscription created",
			"Your subscription was created and is active",
			"from@from.dev",
			[subscription.profile.user.email],
			fail_silently=False,
		)

	return


def customer_subscription_deleted(request):
	subscription = Subscription.objects.get(
		stripe_subscription_id=request["id"]
	)

	if request["status"] == "canceled":
		canceled_at = datetime.utcfromtimestamp(
			int(request["canceled_at"])).strftime('%Y-%m-%d %H:%M:%S')

		subscription.is_active = False
		subscription.canceled_at = canceled_at
		subscription.save()

		send_mail(
			"Subscription canceled",
			"Your subscription was canceled",
			"from@from.dev",
			[subscription.profile.user.email],
			fail_silently=False,
		)

	return


dispatch = {
	"customer_subscription_created": customer_subscription_created,
	"customer_subscription_deleted": customer_subscription_deleted,
}
