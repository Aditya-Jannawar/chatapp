from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('', views.login_view, name='login'),
    path('friend/<str:pk>', views.detail, name="detail"),
    path('sent_msg/<str:pk>', views.sentMessages, name="sent_msg"),
    path('rec_msg/<str:pk>', views.receivedMessages, name="rec_msg"),
    path('notification', views.chatNotification, name="notification"),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
]
