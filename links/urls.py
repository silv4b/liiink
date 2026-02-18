from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("perfil/", views.profile, name="profile"),
    path("excluir-conta/", views.delete_account, name="delete_account"),
    path("delete/<int:link_id>/", views.delete_link, name="delete_link"),
    path("edit/<int:link_id>/", views.edit_link, name="edit_link"),
    path("set-theme/", views.set_theme_preference, name="set_theme_preference"),
    path("<str:username>/", views.public_profile, name="public_profile"),
    path("", views.home, name="home"),
]
