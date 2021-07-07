from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'rooms'

router=DefaultRouter()
router.register('rooms', views.RoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('memberships', views.MembershipListCreateView.as_view())
    ]
