from django.urls import path
from .views import PostListView,PostDetailsView,PostEditView

urlpatterns = [
    path('',PostListView.as_view(),name='post-list'),
    path('post/<int:pk>',PostDetailsView.as_view(),name='post-detail'),
    path('post/edit/<int:pk>',PostEditView.as_view(),name='post-edit'),
]
