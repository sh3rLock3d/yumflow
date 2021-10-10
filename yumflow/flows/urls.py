from rest_framework import routers
from .api import FlowViewSet, DataFrameViewSet

router = routers.DefaultRouter()
router.register('api/flows', FlowViewSet, 'flows')
router.register('api/dataframes', DataFrameViewSet, 'dataframes')

urlpatterns = router.urls