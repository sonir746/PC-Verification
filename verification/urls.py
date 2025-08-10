from django.urls import path
from . import views

urlpatterns = [
    path("",views.verify_page,name='verify_page'),

    path('verify-user/', views.verify_user, name='verify_user'),

]
