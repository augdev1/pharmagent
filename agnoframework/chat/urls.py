from django.urls import path
from . import views

urlpatterns = [
    path('', views.new_chat, name='new_chat'),
    path('chat/<int:conversation_id>/', views.index, name='index'),
    path('chat/<int:conversation_id>/get_response/', views.get_response, name='get_response'),
    path('chat/<int:conversation_id>/delete/', views.delete_chat, name='delete_chat'),
]