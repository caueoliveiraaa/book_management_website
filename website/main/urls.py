from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register, name="register"),
    path("show_users/", views.show_users, name="show_users"),
    path("del_users/", views.del_users, name="del_users"),
    path("show_books/", views.show_books, name="show_books"),
    path("add_books/", views.add_books, name="add_books"),
    path("del_books/", views.del_books, name="del_books"),
    path('logout_user/', views.logout_user, name='logout_user'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
