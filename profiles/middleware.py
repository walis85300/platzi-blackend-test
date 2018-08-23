from django.shortcuts import redirect
from django.urls import reverse

class UserHasProfileMiddlware:

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):

		if not request.user.is_staff:
			if not request.user.is_anonymous:
				if hasattr(request.user, 'profile'):
					profile = request.user.profile
					if not profile.website or not profile.phone_number:
						if request.path not in [reverse('profiles:update'), reverse('profiles:logout')]:
							return redirect('profiles:update')
				else:
					if request.path not in [reverse('profiles:update'), reverse('profiles:logout')]:
						return redirect('profiles:update')

		
		response = self.get_response(request)

		return response
