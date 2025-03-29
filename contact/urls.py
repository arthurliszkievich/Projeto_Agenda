from django.urls import path
from contact import views


# Este app_name é utilizado para previnir conflitos ao criar templates de mesmo nome em diferentes apps. (app_name:nome_do_template)
app_name = "contact"


urlpatterns = [
    path("search/", views.search, name="search"),
    path("", views.index, name="index"),
    # CRUD contact
    path("contact/<int:contact_id>/detail/", views.contact, name="contact"),
    path("contact/create/", views.create, name="create"),
    path("contact/<int:contact_id>/update/", views.update, name="update"),
    path("contact/contact/<int:contact_id>/delete/", views.delete, name="delete"),
    # user
    path("user/create/", views.register, name="register"),
    path("user/login/", views.login_view, name="login"),
    path("user/logout/", views.logout_view, name="logout"),
    path("user/update/", views.user_update, name="user_update"),
]
