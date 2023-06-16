from rest_framework.routers import SimpleRouter
from .views import UserViewSet, ReviewViewSet, TestingViewSet, QuestionViewSet, SectionViewSet, LessonViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='user')
router.register('testing', TestingViewSet)
router.register('question', QuestionViewSet)
router.register(r'reviews', ReviewViewSet)
router.register('sections', SectionViewSet)
router.register('lessons', LessonViewSet)
urlpatterns = [
]