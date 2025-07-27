from rest_framework_nested import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')

conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.registers.NestedDefault(router, r'conversation=message')


router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
	path('', include(router.urls)),
 path('', include(conversations_router.urls)),
]