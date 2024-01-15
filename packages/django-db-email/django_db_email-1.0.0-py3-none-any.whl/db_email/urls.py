from django.urls import path

from db_email import views


app_name = 'db_email'


urlpatterns = [
    path('html_message/<int:email_id>', views.html_message, name='html_message'),
]
