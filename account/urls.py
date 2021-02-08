from django.urls import path
from . import views


urlpatterns = [
    
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('home/',views.userPage,name="home"),
    path('',views.userPage,name="user"),
    path('user/',views.userPage,name="user"),
    path('adminPage/',views.adminPage,name="adminPage"),
    path('sharefile/',views.sharefile,name="sharefile"),
    path('yourfiles/',views.yourfiles,name="yourfiles"),
    path('delete/<file_id>',views.deletefile,name="deletefile"),
    path('edit/<file_id>',views.edit,name="editfile"),
    path('sharedfiles/',views.sharedfiles,name="sharedfiles"),
    path('file/<file_id>',views.file,name="file"),
    path('file/<file_id>/comment/delete/<comment_id>',views.deletecomment,name="deletecomment"),
    path('file/<file_id>/comment/edit/<comment_id>',views.editcomment,name="editcomment"),
]