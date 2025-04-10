from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('', views.class_list, name='class_list'),
    path('<int:class_id>/', views.class_detail, name='class_detail'),
    path('book/<int:schedule_id>/', views.book_class, name='book_class'),
] 