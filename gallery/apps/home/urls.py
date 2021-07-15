from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('upload-image/', views.UploadView.as_view(), name="upload"),
    path('approve/<int:pk>/', views.ApproveView.as_view(), name="approve"),
    path('like/<int:pk>/', views.LikeView.as_view(), name="like"),
    path('comment/', views.CommentView.as_view(), name="comment"),
]