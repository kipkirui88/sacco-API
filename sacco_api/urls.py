from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, CheckBalanceView, WithdrawSavingsView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create a schema view for Swagger documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Sacco API",
      default_version='v1',
      description="API for managing Sacco members and savings",
      terms_of_service="https://www.koel.com/terms/",
      contact=openapi.Contact(email="hezekiahkoech@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'savings', MemberViewSet, basename='savings')

urlpatterns = [
    path('', include(router.urls)),
    path('member/<str:membership_number>/', MemberViewSet.as_view({'get': 'retrieve_by_membership_number'}), name='member-by-membership'),
    path('members/<int:pk>/create_savings/', MemberViewSet.as_view({'post': 'create_savings'}), name='member-create-savings'),
    path('members/<int:pk>/check_balance/', CheckBalanceView.as_view(), name='check_balance'),
    path('members/<int:pk>/withdraw_savings/', WithdrawSavingsView.as_view(), name='withdraw_savings'),
    
    # Swagger documentation URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
