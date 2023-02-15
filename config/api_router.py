from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from djsniper.users.api.views import UserViewSet
from djsniper.sniper.views import ProjectViewset, CategoryViewset, OrdersViewset

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("projects", ProjectViewset)
router.register("categories", CategoryViewset)
router.register("orders", OrdersViewset)

app_name = "api"
urlpatterns = router.urls
