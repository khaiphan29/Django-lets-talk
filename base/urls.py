from django.urls import path
from . import views

urlpatterns = [
    path('login', views.userLogin, name="login"),
    path('logout', views.userLogout, name="logout"),
    path('register', views.userRegister, name="register"),

    path('', views.home, name="home"), 
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.profile, name="profile"),

    path('create-room/', views.createRoom, name="create_room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    #rest api
    path('search-room', views.search_room, name="search-room")
]
