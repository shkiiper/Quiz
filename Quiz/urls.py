from django.urls import path, include
from .routers import router
from .views import TokenObtainPairView, PerformanceView

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/performance/', PerformanceView.as_view(), name='performance'),
]