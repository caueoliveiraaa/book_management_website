from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register, name="register"),
    path("reserve_book/<int:book_id>/", views.reserve_book, name="reserve_book"),
    path("take_book/<int:book_id>/<int:reservation_id>/", views.take_book, name="take_book"),
    path("show_users/", views.show_users, name="show_users"),
    path("del_users/<int:user_id>/", views.del_users, name="del_users"),
    path("return_book/<int:book_id>/<int:reservation_id>/", views.return_book, name="return_book"),
    path("show_books/filter/", views.show_books_filter, name="show_books_filter"),
    path("add_books/", views.add_books, name="add_books"),
    path("update_book_status/<int:book_id>/", views.update_book_status, name="update_book_status"),
    path("cancel_reservation/<int:reservation_id>/", views.cancel_reservation, name="cancel_reservation"),
    path("del_books/<int:book_id>/", views.del_books, name="del_books"),
    path('logout_user/', views.logout_user, name='logout_user'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
