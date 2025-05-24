from rest_framework.routers import DefaultRouter

from .views import SectionViewSet, SubsectionViewSet, TestViewSet

router = DefaultRouter()
router.register(r"sections", SectionViewSet)
router.register(r"subsections", SubsectionViewSet)
router.register(r"tests", TestViewSet)

urlpatterns = router.urls
