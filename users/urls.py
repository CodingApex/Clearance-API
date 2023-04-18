from django.urls import path, include
from . import views
from users.views import GoogleLogin

urlpatterns = [
    path('', views.api_root),
    path('Registrar/', views.APIRegistrarViews.as_view(), name='registrar'),
    path('Clerk/', views.APIClerkView.as_view(), name='clerk'),
    path('Clerk/<str:pk>/', views.APIClerkUpdate.as_view()),
    path('account/google/', GoogleLogin.as_view(), name='google_login')
]