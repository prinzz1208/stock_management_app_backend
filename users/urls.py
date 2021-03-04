from django.urls import path

from users.views import index, signup, login

urlpatterns = [
    path('', index),
    path('signup', signup),
    path('login', login)
]
