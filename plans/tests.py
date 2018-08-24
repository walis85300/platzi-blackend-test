from django.test import TestCase

from .models import Plan, Subscription

# Create your tests here.


class PlansTests(TestCase):

	def test_subscribe_user(self):
		plan = Plan.objects.create(
			description='Annual',
			price=299.00,
			stripe_plan_id='plan_DTNUd2nXDz7v5k',
			is_annual=True)

		self.client.post('/users/signup/', {
			'username': 'testusername',
			'password': '123456',
			'password_confirmation': '123456',
			'first_name': 'test',
			'last_name': 'last test',
			'email': 'test@test.com',
			'website': 'https://testsite.dev',
			'phone_number': '123456',
			'stripe_token': 'tok_visa'},
			follow=True)

		login = self.client.login(username='testusername', password='123456')

		self.assertTrue(login)

		response = self.client.post('/plans/subscription/subscribe',
									{'plan_id': 'plan_DTNUd2nXDz7v5k'}, follow=True)

		self.assertEqual(response.status_code, 200)

		subscription = Subscription.objects.all()[:1].get()

		response = (self
					.client
					.post('/plans/subscription/cancel', 
							{'subscription_id': subscription.stripe_subscription_id},
							follow=True))
		self.assertEqual(response.status_code, 200)
