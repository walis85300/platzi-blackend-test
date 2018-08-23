from django.contrib import admin

from .models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('pk', 'user', 'website', 'phone_number')
	list_display_links = ('pk',)
	search_fields = ('user__email',)

	list_filter = (
		'created_at',
		'updated_at',
		'user__is_active'
	)
