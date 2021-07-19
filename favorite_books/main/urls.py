from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home),
    path('create', views.home_create),
    path('dashboard', views.dashboard),
    path('log', views.log_user),
    path('logout', views.logout),
    path('add_book', views.add_book),
    path('show_book/<int:book_id>', views.show),
    path('favorite/<int:book_id>', views.favorite),
    path('unfavorite/<int:book_id>', views.unfavorite),
    path('update/<int:book_id>', views.update),
    path('delete/<int:book_id>', views.delete),
]