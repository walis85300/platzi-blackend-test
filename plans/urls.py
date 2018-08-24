from django.urls import path
from plans import views

urlpatterns = [
	path(
		route="subscription/cancel",
		view=views.CancelSubscriptionView.as_view(),
		name='cancel_subscription'
	),
	path(
		route="subscription/subscribe",
		view=views.CreateSubscriptionView.as_view(),
		name='create_subscription'
	)
]
