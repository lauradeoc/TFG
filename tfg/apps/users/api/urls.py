from django.urls import path
from apps.users.api.api import MlrParamViewSet, SurveyingViewSet, create_model_view, user_api_view,user_detail_api_view,result_detail,result_list,surveying,create_model_view,create_model_view2,graficas
from apps.users.api.api import SurveyingApiView
from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from apps.users.api.api import MlrModelViewSet, MlrProjectViewSet,MlrParamViewSet,MlrReportViewSet,MlrResultViewSet,MlrGraphViewSet,SurveyingApiView

#from apps.users.api.api import MlrExecutionViewSet
urlpatterns=[
    path('usuario/',user_api_view, name='usuario_api'),
    path('usuario/<int:pk>/',user_detail_api_view, name='usuario_detail_api_view'),
    #path('param/',param_api_view, name='param_api'),
    #path('param/<int:pk>/',param_detail_api_view, name='param_detail_api'),
    #path('project/',project_list,name='project_api'),
    #path('project/<int:pk>/',project_detail,name='project_detail_api'),
    path('result/',result_list,name='result_api'),
    path('result/<int:pk>/',result_detail,name='result_detail_api'),
    path('execute/',surveying,name='execute'),
    path('create/',create_model_view,name='create'),
    path('create2/',create_model_view2,name='create2'),
    path('graficas/',graficas,name='graficas'),
    #path('surveying/',SurveyingApiView.as_view(),name='surveying'),


]

#router = DefaultRouter()
#router.register(r'usuarios',MlrModelViewSet)

#urlpatterns = router.urls



router = DefaultRouter()
router.register("mlr_models", MlrModelViewSet, basename="mlr_models")
router.register("mlr_projects", MlrProjectViewSet, basename="mlr_projects")
router.register("mlr_params", MlrParamViewSet, basename="mlr_params")
router.register("mlr_report", MlrReportViewSet, basename="mlr_report")
router.register("mlr_result", MlrResultViewSet, basename="mlr_result")
router.register("mlr_graphs", MlrGraphViewSet, basename="mlr_graph")
router.register("surveying", SurveyingViewSet, basename="surveying")
#router.register("mlr_executing", MlrExecutionViewSet, basename="mlr_executing")


mlr_model_urlpatterns = [url("api/v1/", include(router.urls))]