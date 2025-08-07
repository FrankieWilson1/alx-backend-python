from rest_framework_nested import routers

from .views import UserViewSet, ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'conversations', ConversationViewSet)

conversations_router = routers.NestedSimpleRouter(
    router,
    r'conversations',
    lookup='conversation'
)
conversations_router.register(
    r'messages',
    MessageViewSet,
    basename='conversation-messages'
)

urlpatterns = router.urls
urlpatterns += conversations_router.urls
