from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter
from .views import KenyaSubcountyViewSet, KenyaCountryViewSet, KenyaCountyViewSet, map_view, HospitalsViewSet, Level4BufferViewSet, Level5BufferViewSet, analytics_view, buffer, get_hospital_stats, get_buffer_distances, count_hospitals_in_buffer

router = DefaultRouter()
router.register(r'subcounties', KenyaSubcountyViewSet)
router.register(r'countries', KenyaCountryViewSet)
router.register(r'counties', KenyaCountyViewSet)
router.register(r'hospitals', HospitalsViewSet)
router.register(r'level4-buffer', Level4BufferViewSet, basename='level4-buffer')
router.register(r'level5-buffer', Level5BufferViewSet, basename='level5-buffer')

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path("api/", include(router.urls)),
    path('map/', map_view, name='map_view'),
    path('home/analytics.html', analytics_view, name='analytics'),
    path('home/analytics.html', buffer, name='analytics'),
    path('home/get-hospital-stats/', get_hospital_stats, name='get_hospital_stats'),
    path('home/analytics/', analytics_view, name='analytics'),
    path('home/buffer/', buffer, name='buffer'),
    path('home/get-buffer-distances/', get_buffer_distances, name='get_buffer_distances'),
    path('home/count-hospitals-in-buffer/', count_hospitals_in_buffer, name='count_hospitals_in_buffer'),
]