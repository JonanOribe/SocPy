from django.urls import path
from .views import PostListView,PostDetailsView

urlpatterns = [
    path('',PostListView.as_view(),name='post-list'),
    path('post/<int:pk>',PostDetailsView.as_view(),name='post-detail')
]
