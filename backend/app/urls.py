from django.urls import path
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
# Import views for better organization
from app.views import (
    # Authentication views
    login_view, register_view, logout_view, api_login, api_register,

    # Main app views
    home, crops, uploads, profiledata, contact_view, forgot_pass,

    # API views
    predict_simple, disease_details, translate_text, health_check,
    dashboard_stats, farmer_dashboard,

    # Marketplace views
    marketplace_products, mandi_locations, verify_product_quality, create_product_inquiry,

    # Weather and notifications
    get_weather_data, get_weather_forecast,
    get_user_notifications, create_notification,
    update_notification_preferences, get_notification_preferences,

    # Error handling
    my_404_page
)

handler404 = my_404_page

@ensure_csrf_cookie
def csrf(request):
    """Issue a CSRF cookie for the React client before state-changing calls."""
    return JsonResponse({'csrfToken': get_token(request)})

@require_GET
def metrics(request):
    """Internal Prometheus scrape endpoint; Nginx deliberately does not publish it."""
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)

urlpatterns = [
    path('',home,name="home"),
    path('upload/', uploads, name='upload'),
    path('crops/',crops,name="crops"),
    path('crops/disease/<slug:oneDisease>/', crops, name='oneDisease'),
    path('forgot-password/',forgot_pass,name="forgot"),
    path('register/',register_view,name="register"),
    path('contact/', contact_view, name='contact'),
    path('login/',login_view,name="login"),
    path('logout/',logout_view, name='logout'),
    path('user/profile/<int:pk>/',profiledata, name='profile'),
    path('api/predict/', predict_simple, name='api_predict'),
    path('api/disease/<str:disease_name>/', disease_details, name='disease_details'),
    path('api/translate/', translate_text, name='translate_text'),
    path('api/dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    path('api/dashboard/farmer/', farmer_dashboard, name='farmer_dashboard'),
    path('api/auth/login/', api_login, name='api_login'),
    path('api/auth/register/', api_register, name='api_register'),
    path('api/marketplace/products/', marketplace_products, name='marketplace_products'),
    path('api/marketplace/mandis/', mandi_locations, name='mandi_locations'),
    path('api/marketplace/verify-quality/', verify_product_quality, name='verify_product_quality'),
    path('api/marketplace/inquiry/', create_product_inquiry, name='create_product_inquiry'),

    # Weather and Notifications
    path('api/weather/current/', get_weather_data, name='get_weather_data'),
    path('api/weather/forecast/', get_weather_forecast, name='get_weather_forecast'),
    path('api/notifications/', get_user_notifications, name='get_user_notifications'),
    path('api/notifications/create/', create_notification, name='create_notification'),
    path('api/notifications/preferences/', get_notification_preferences, name='get_notification_preferences'),
    path('api/notifications/preferences/update/', update_notification_preferences, name='update_notification_preferences'),

    # Health check for Render monitoring
    path('api/health/', health_check, name='health_check'),
    path('api/csrf/', csrf, name='csrf'),
    path('metrics', metrics, name='metrics'),
]
