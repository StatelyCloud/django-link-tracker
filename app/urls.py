from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create/', views.create_profile_view, name='create_profile'),
    path('<slug:slug>/', views.profile_detail, name='profile_detail'),
    path('<slug:slug>/edit/', views.profile_edit, name='profile_edit'),
    path('<slug:slug>/add-link/', views.add_link, name='add_link'),
    path('<slug:slug>/delete-link/<int:link_id>/', views.delete_link_view, name='delete_link'),
    path('<slug:slug>/update-order/', views.update_link_order, name='update_link_order'),
    path('<slug:slug>/link/<int:link_id>/', views.link_redirect, name='link_redirect'),
]