from django.urls import path
from . import views
from .views import RequestAdminApprovalView

urlpatterns = [
    path('create_post/<str:post_type>/', views.create_post, name='create_post'),
    path('update_post/<int:post_id>/<str:post_type>/', views.update_post, name='update_post'),
    path('delete_post/<int:post_id>/<str:post_type>/', views.delete_post, name='delete_post'),
    # path('request_approval/', views.request_admin_approval, name='request_approval'),
    path('request-approval/', RequestAdminApprovalView.as_view(), name='request_approval'),
]
