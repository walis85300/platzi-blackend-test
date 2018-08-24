from django.urls import path
from profiles import views

urlpatterns = [
    path(
        route='login/',
        view=views.LoginUserView.as_view(),
        name='login'),

    path(
        route='logout/',
        view=views.LogoutUserView.as_view(),
        name='logout'),

    path(
        route='signup/',
        view=views.SignupUserView.as_view(),
        name='signup'),


    path(
        route='me',
        view=views.MeProfileView.as_view(),
        name='me_profile'),

    path(
        route='profile/update',
        view=views.UpdateProfileView.as_view(),
        name='update'),

    path(
        route='<str:username>/',
        view=views.DetailProfileView.as_view(),
        name='detail')
]
