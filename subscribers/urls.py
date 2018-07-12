from django.conf.urls import url

from subscribers import views

urlpatterns = [
    url(r'^form/', views.view_form, name='view_form'),
    url(r'^message/', views.message, name='message'),
    url(r'^notify/', views.notify, name='send_notifications'),
]
