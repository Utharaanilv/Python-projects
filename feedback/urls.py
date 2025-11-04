from django.urls import path
from . import views

urlpatterns = [
    # Page where user gives feedback (with rating, comment, optional image)
    path('give/', views.give_feedback, name='give_feedback'),

    # Page where user can view their past feedback
    path('my/', views.my_feedback_view, name='my_feedback'),

    # Edit feedback
    path('edit/<int:feedback_id>/', views.edit_feedback_view, name='edit_feedback'),

    # Delete feedback
    path('delete/<int:feedback_id>/', views.delete_feedback_view, name='delete_feedback'),
]