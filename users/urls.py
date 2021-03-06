from django.urls import path

from users.views import index, signup, login, AuthenticatedUser, logout

urlpatterns = [
    path('', index),
    path('signup', signup),
    path('login', login),
    path('logout', logout),
    path('user', AuthenticatedUser.as_view())
]
