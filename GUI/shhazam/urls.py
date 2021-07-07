from django.urls import path
# import views from local directory.
from . import views
urlpatterns = [
    # When user request home page http://localhost:8000/my_hello_world, it will invoke the home function defined in views.py.
    path('', views.index_page, name='index'),
    path('song-list/', views.song_list, name='song_list'),
]

