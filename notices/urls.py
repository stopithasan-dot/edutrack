from django.urls import path
from . import views

urlpatterns = [
    path('notices/', views.NoticeListView.as_view(), name='notice_list'),
    path('notices/post/', views.NoticeCreateView.as_view(), name='notice_add'),
    path('notices/<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='notice_delete'),
]
