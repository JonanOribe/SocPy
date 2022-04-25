from django.urls import path
from .views import CommentDeleteView, PostDeleteView, PostListView,PostDetailsView,PostEditView

urlpatterns = [
    path('',PostListView.as_view(),name='post-list'),
    path('post/<int:pk>',PostDetailsView.as_view(),name='post-detail'),
    path('post/edit/<int:pk>',PostEditView.as_view(),name='post-edit'),
    path('post/delete/<int:pk>',PostDeleteView.as_view(),name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/',CommentDeleteView.as_view(),name='comment-delete'),
]
