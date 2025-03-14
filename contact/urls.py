from django.urls import path
from contact import views


# Este app_name é utilizado para previnir conflitos ao criar templates de mesmo nome em diferentes apps. (app_name:nome_do_template)
app_name = 'contact'


urlpatterns = [
    path('', views.index, name='index'),
]
