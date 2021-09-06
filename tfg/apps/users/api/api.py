from datetime import datetime
from django.db.models.base import Model
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.api.serializers import MlrSVCModel, UserSerializer, ExecutionSerializer,MlrParams
from rest_framework import viewsets


from models_surveying.surveying_models.surveying_model import SurveyingModel
from models_surveying.helpers import metrics_helper as Metrics


### Vista para la ejecución del modelo
class SurveyingApiView(APIView):
    serializer_class=ExecutionSerializer

    def get(self, request, format=None):
        an_api_view=['Vista para le ejecución de modelos']

        return Response({'message':'Hello','an_api_view':an_api_view})

    def post(self,request):
        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
            model_path=serializer.validated_data.get('model_path')

            message=f'La ruta es: {model_path}'

            return Response({'message':message})

        else:
            Response(serializer.errors,status=status.status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return Response({'method': 'PUT'})

    def patch(self,request,pk=None):
        return Response({'method': 'PATCH'})
    
    def delete(self,request,pk=None):
        return Response({'method': 'DELETE'})



class SurveyingViewSet(viewsets.ViewSet):
    serializer_class=ExecutionSerializer

    def list(self, request):
        a_viewset=['Vista encargada de la ejecución de los modelos']

        return Response({'message': 'Hola!', 'a_view_set':a_viewset})


    def create(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            model_path=serializer.validated_data.get('model_path')
            _matrix_name=serializer.validated_data.get('_matrix_name')
            _class_name=serializer.validated_data.get('_class_name')
            _train_matrix_path=serializer.validated_data.get('_train_matrix_path')
            _result_path=serializer.validated_data.get('_result_path')
            _test_size=serializer.validated_data.get('_test_size')
            _random_state=serializer.validated_data.get('_random_state')
            _sampling_strategy=None
            _features=serializer.validated_data.get('_features')

            surveying_model = SurveyingModel(
                model_path,
                _matrix_name,
                _features,
                _class_name,
                _train_matrix_path,
                _result_path,
                _test_size,
                _random_state,
                _sampling_strategy
            )

            ### Executing the classification
            result = surveying_model.Classify()
            #message=""
            
            for metric in Metrics.score_metrics:
                m=MlrResult.objects.create(name=metric,value=result.TrainResult[metric],mlr_report='')

            for metric in Metrics.score_metrics:
                m=MlrResult.objects.create(name=metric,value=result.TestResult[metric],mlr_report='')

            message=f'Modelo ejecutado correctamente:'
            #message=f'La ruta es: {_sampling_strategy}'
            

            return Response({'message':message})

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 


    def retrieve(self,request,pk=None):
        return Response({'http_method': 'GET'})

    def update(self,request,pk=None):
        return Response({'http_method': 'PUT'})

    def partial_update(self,request,pk=None):
        return Response({'http_method': 'PATCH'})

    def destroy(self,request,pk=None):
        return Response({'http_method': 'DELETE'})



@api_view(['GET','POST'])
def user_api_view(request):
    #list
    if request.method == 'GET':
        #queryset
        users = User.objects.all()
        users_serializer=UserSerializer(users,many=True)
        return Response(users_serializer.data,status = status.HTTP_200_OK)

    #create
    elif request.method == 'POST':
        user_serializer = UserSerializer(data = request.data)
        # validation
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message':'Usuario creado correctamente!'},status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def user_detail_api_view(request,pk=None):
    # queryset
    user = User.objects.filter(id=pk).first()

    #validation
    if user:

        #retrieve
        if request.method == 'GET':
            user_serializer=UserSerializer(user)
            return Response(user_serializer.data,status = status.HTTP_200_OK)

        #update
        elif request.method == 'PUT': ## actualizar
            user_serializer=UserSerializer(user,data=request.data)

            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data,status = status.HTTP_200_OK)

            return Response(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        #delete
        elif request.method == 'DELETE':
            user.delete()
            return Response({'message':'Usuario Eliminado Correctamente!'},status = status.HTTP_200_OK)

    return Response({'message':'No se ha encontrado un usuario con estos datos'},status=status.HTTP_400_BAD_REQUEST)


from apps.users.models import MlrGraph
from apps.users.api.serializers import GraphSerializer
from models_reports.factories.graph_factory import GraphFactory

class MlrGraphViewSet(viewsets.ModelViewSet):
    serializer_class = GraphSerializer
    queryset = MlrGraph.objects.all()

    def list(self, request):
        a_viewset=['Vista encargada de la obtención de las gráficas']
        return Response({'message': 'Hola!', 'a_view_set':a_viewset})

    def get_queryset(self):
        #return self.queryset.filter(created_by=self.request.user)
        return self.queryset

    def create(self,request):
        ###
        save_path = 'report/'
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            title=serializer.validated_data.get('title')
            save_path=serializer.validated_data.get('save_path')
            mlr_model=serializer.validated_data.get('mlr_model')

            serializer.save(mlr_model=mlr_model)


            #title = 'Title ROC'
            save_path =  'report/'
            x_train_path = 'result/train_features.csv'
            y_train_path = 'result/train_label.csv'
            x_test_path = 'result/test_features.csv'
            y_test_path = 'result/test_label.csv'
                
            model_path = 'new_model/SVC_Model_04092021180745_fitted'

            factory = GraphFactory(x_train_path, y_train_path, x_test_path, y_test_path, model_path)

            factory.GenerateRocAucGraph(title, save_path)

            #factory.GeneratePRCGraph("PCR plot", save_path)

            message=f'Nombre de la grafica: {title}'
          

            return Response({'message':message})


        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 


"""@api_view(['GET', 'POST'])
def graph_list(request):
    if request.method == 'GET':
        data = MlrGraph.objects.all()

        serializer = GraphSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GraphSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def graph_detail(request, pk):
    try:
        param = MlrGraph.objects.get(pk=pk)
    except MlrGraph.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = GraphSerializer(param, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        param.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""

# -----------------------------------------------------------------------#
from models_creator.model_factory import ModelFactory
from models_creator import model_name as model
import json

from apps.users.models import MlrModel
from apps.users.api.serializers import ModelSerializer

class MlrModelViewSet(viewsets.ModelViewSet):
    serializer_class = ModelSerializer
    queryset = MlrModel.objects.all()

    """def list(self, request):
        a_viewset=['Vista encargada de la creación de los modelos']

        return Response({'message': 'Hola!', 'a_view_set':a_viewset})"""

    def perform_create(self, serializer):
       # serializer.save(created_by=self.request.user)
       local_path = "new_model/"
       serializer = self.serializer_class(data=self.request.data)
       dc={}
       if serializer.is_valid():
            model_name=serializer.validated_data.get('model_name')
            new_model_file_path=serializer.validated_data.get('new_model_file_path')
            fitted_model_file_path=serializer.validated_data.get('fitted_model_file_path')
            params=serializer.validated_data.get('params')
            dc=json.loads(params)
            svc=serializer.save(created_by=self.request.user)
            for key in dc:
                p=MlrParams.objects.create(name=key,value=dc[key],mlr_model=svc)
            # Creamos el fichero .joblib
            factory = ModelFactory(model.SVC,local_path)
            factory.Create(dc)

      
    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

  

"""class SurveyingViewSet(viewsets.ViewSet):
    serializer_class=ExecutionSerializer

    def list(self, request):
        a_viewset=['Vista encargada de surveying']

        return Response({'message': 'Hola!', 'a_view_set':a_viewset})"""


# -----------------------------------------------------------------------#


from apps.users.models import MlrParams
from apps.users.api.serializers import ParamSerializer


class MlrParamViewSet(viewsets.ModelViewSet):
    serializer_class = ParamSerializer
    queryset = MlrParams.objects.all()

    def perform_create(self, serializer):
        #serializer.save(created_by=self.request.user)
        serializer.save()

    def get_queryset(self):
        #return self.queryset.filter(created_by=self.request.user)
        return self.queryset

"""@api_view(['GET', 'POST'])
def param_list(request):
    if request.method == 'GET':
        data = MlrParams.objects.all()

        serializer = ParamSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ParamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def user_api_view(request):
    #list
    if request.method == 'GET':
        #queryset
        params = MlrParams.objects.all()
        params_serializer=ParamSerializer(params,many=True)
        return Response(params_serializer.data,status = status.HTTP_200_OK)

    #create
    elif request.method == 'POST':
        params_serializer = ParamSerializer(data = request.data)
        # validation
        if params_serializer.is_valid():
            params_serializer.save()
            return Response({'message':'Parámetro creado correctamente!'},status=status.HTTP_201_CREATED)

        return Response(params_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def param_detail(request, pk):
    try:
        param = MlrParams.objects.get(pk=pk)
    except MlrParams.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ParamSerializer(param, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        param.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""

# -----------------------------------------------------------------------#

from apps.users.models import MrlProfile
from apps.users.api.serializers import ProfileSerializer

@api_view(['GET', 'POST'])
def profile_list(request):
    if request.method == 'GET':
        data = MrlProfile.objects.all()

        serializer = ProfileSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
def profile_detail(request, pk):
    try:
        param = MrlProfile.objects.get(pk=pk)
    except MrlProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProfileSerializer(param, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        param.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------------------------------#

from apps.users.models import MlrProject
from apps.users.api.serializers import ProjectSerializer


class MlrProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = MlrProject.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

"""@api_view(['GET', 'POST'])
def project_list(request):
    #list
    if request.method == 'GET':
        #queryset
        Project = MlrProject.objects.all()
        Project_serializer=ProjectSerializer(Project,many=True)
        return Response(Project_serializer.data,status = status.HTTP_200_OK)

    #create
    elif request.method == 'POST':
        Project_serializer = ProjectSerializer(data = request.data)
        # validation
        if Project_serializer.is_valid():
            Project_serializer.save()
            return Response({'message':'Proyecto creado correctamente!'},status=status.HTTP_201_CREATED)

        return Response(Project_serializer.errors,status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET','PUT','DELETE'])
def project_detail(request,pk=None):
    # queryset
    Project = MlrProject.objects.filter(id=pk).first()

    #validation
    if Project:

        #retrieve
        if request.method == 'GET':
            Project_serializer=ProjectSerializer(Project)
            return Response(Project_serializer.data,status = status.HTTP_200_OK)

        #update
        elif request.method == 'PUT': ## actualizar
            Project_serializer=ProjectSerializer(Project,data=request.data)

            if Project_serializer.is_valid():
                Project_serializer.save()
                return Response(Project_serializer.data,status = status.HTTP_200_OK)

            return Response(Project_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        #delete
        elif request.method == 'DELETE':
            Project.delete()
            return Response({'message':'Proyecto Eliminado Correctamente!'},status = status.HTTP_200_OK)

    return Response({'message':'No se ha encontrado un proyecto con estos datos'},status=status.HTTP_400_BAD_REQUEST)
"""
# -----------------------------------------------------------------------#

from apps.users.models import MlrReport
from apps.users.api.serializers import ReportSerializer

from models_reports.report_provider.report_provider import ReportProvider

from models_reports.csv_report.csv_arguments import CsvArguments
from models_reports.txt_report.txt_arguments import TxtArguments



class MlrReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = MlrReport.objects.all()

    def list(self, request):
        a_viewset=['Vista encargada de la obtención de los reportes']
        return Response({'message': 'Hola!', 'a_view_set':a_viewset})

    def get_queryset(self):
        #return self.queryset.filter(created_by=self.request.user)
        return self.queryset

    def create(self,request):
        ###
        report_path = 'report/'
        name = 'Resultado'
        metrics_result = {'accuracy_train': 0.9282914336486698, 
                    'roc_auc_train': 0.8551730349196858, 
                    'precision_train': 1.0, 
                    'recall_train': 0.003269160915365057, 
                    'f1_train': 0.006515083257307421, 
                    'average_precision_train': 0.45472984064068067,
                    'accuracy_test': 0.9280861294031568, 
                    'roc_auc_test': 0.6524753664905696, 
                    'precision_test': 0.1, 
                    'recall_test': 0.00014534883720930232, 
                    'f1_test': 0.0002902757619738752, 
                    'average_precision_test': 0.1265774502989742}

        params = {'learning_rate': 0.04183772129568829, 'max_depth': 4, 'min_child_weight': 0.4837592199226932, 'n_estimators': 500, 'reg_alpha': 0.7580454954856516, 'reg_lambda': 0.9626867478901874, 'scale_pos_weight': 0.4541587512627421}
        ###
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            type=serializer.validated_data.get('type')
            path=serializer.validated_data.get('path')
            mlr_model=serializer.validated_data.get('mlr_model')

        
            serializer.save(mlr_model=mlr_model)

            csv_args = CsvArguments(report_path, name, metrics_result)
            txt_args = TxtArguments(report_path, name, params, metrics_result)

            provider = ReportProvider()

            provider.GenerateCsvReport(csv_args)

            provider.GenerateTxtReport(txt_args)

            message=f'Nombre del report: {name}'
            #message=f'Los parametros son: {params.split(", ")}'
            #message=f'Los parametros son: {params.replace("{","")}'
          

            return Response({'message':message})


        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 


"""@api_view(['GET', 'POST'])
def report_list(request):
    if request.method == 'GET':
        data = MlrReport.objects.all()

        serializer = ReportSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def report_detail(request, pk):
    try:
        param = MlrReport.objects.get(pk=pk)
    except MlrReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ReportSerializer(param, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        param.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""


# -----------------------------------------------------------------------#

from apps.users.models import MlrResult
from apps.users.api.serializers import ResultSerializer


class MlrResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    queryset = MlrResult.objects.all()

    def perform_create(self, serializer):
        #serializer.save(created_by=self.request.user)
        serializer.save()

    def get_queryset(self):
        #return self.queryset.filter(created_by=self.request.user)
        return self.queryset







"""@api_view(['GET', 'POST'])
def result_list(request):
    if request.method == 'GET':
        data = MlrResult.objects.all()

        serializer = ResultSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def result_detail(request, pk):
    try:
        param = MlrResult.objects.get(pk=pk)
    except MlrResult.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ResultSerializer(param, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        param.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""

# -----------------------------------------------------------------------#
from apps.users.models import MlrResult
from apps.users.api.serializers import ResultSerializer

@api_view(['GET', 'POST'])
def result_list(request):
    if request.method == 'GET':
        data = MlrResult.objects.all()

        serializer = ResultSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def result_detail(request, pk):
    try:
        param = MlrResult.objects.get(pk=pk)
    except MlrResult.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ResultSerializer(param, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        param.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------------------------------#

from apps.users.models import MlrUserRol
from apps.users.api.serializers import UserRolSerializer

@api_view(['GET', 'POST'])
def user_rol_list(request):
    if request.method == 'GET':
        data = MlrUserRol.objects.all()

        serializer = UserRolSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserRolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def user_rol_list_detail(request, pk):
    try:
        param = MlrUserRol.objects.get(pk=pk)
    except MlrUserRol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserRolSerializer(param, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        param.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------------#

from apps.users.models import MlrUserRol
from apps.users.api.serializers import UserRolSerializer

@api_view(['GET', 'POST'])
def user_rol_list(request):
    if request.method == 'GET':
        data = MlrUserRol.objects.all()

        serializer = UserRolSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserRolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def user_rol_list_detail(request, pk):
    try:
        param = MlrUserRol.objects.get(pk=pk)
    except MlrUserRol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserRolSerializer(param, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        param.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#from models_creator.model_factory import ModelFactory
#from models_creator import model_name as model




@api_view(['GET','POST'])
def create_model_view(request):
    #list
    if request.method == 'GET':
        #queryset
        models = MlrModel.objects.all()
        model_serializer=ModelSerializer(models,many=True)
        return Response(model_serializer.data,status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        local_path = "new_model/"
        serializer = ModelSerializer(data = request.data)
        dc={}

        # validation
        if serializer.is_valid():
            model_name=serializer.validated_data.get('model_name')
            new_model_file_path=serializer.validated_data.get('new_model_file_path')
            fitted_model_file_path=serializer.validated_data.get('fitted_model_file_path')
            params=serializer.validated_data.get('params')
            dc=json.loads(params)

            svc=serializer.save(created_by=request.user)

            for key in dc:
                p=MlrParams.objects.create(name=key,value=dc[key],mlr_model=svc)

            # Creamos el fichero .joblib
            factory = ModelFactory(model.SVC,local_path)
            factory.Create(dc)

            #message=f'Los parametros son: {type(params)}'
            message=f'Los parametros son: {dc}'
            #message=f'Los parametros son: {params.split(", ")}'
            #message=f'Los parametros son: {params.replace("{","")}'
         
                
            return Response({'message':'MODELO creado correctamente!'},status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET','POST'])
def create_model_view2(request):
    #list
    if request.method == 'GET':
        #queryset
        models = MlrModel.objects.all()
        model_serializer=ModelSerializer(models,many=True)
        return Response(model_serializer.data,status = status.HTTP_200_OK)
        

    #create
    elif request.method == 'POST':
        model_serializer = MlrSVCModel(data = request.data)
        # validation
        if model_serializer.is_valid():
            #user_serializer.save()
            dc={}
            model_serializer=MlrSVCModel(data=request.data)
            if model_serializer.is_valid(): # validar si la informacion del request es valida para registro
                #model_serializer.save(created_by=request.user)
                # Creamos el modelo con su nombre
                svc=MlrModel.objects.create(model_name=deno)
                # Montamos el diccionario para pasar los parametros al Create. Ademas, creamos los parametros en la bdd
                dc['C']=C
                #p1=Parametros.objects.create(nombre='C',valor=C)
                dc['kernel']=kernel
                #p2=Parametros.objects.create(nombre='kernel',valor=kernel)
                dc['degree']=degree
                #p3=Parametros.objects.create(nombre='degree',valor=degree)
                dc['random_state']=random_state
                #p4=Parametros.objects.create(nombre='random_state',valor=random_state)

                # Creamos el fichero .joblib
                factory = ModelFactory(model.SVC,local_path)
                factory.Create(dc)

                
            return Response({'message':'MODELO creado correctamente!'},status=status.HTTP_201_CREATED)

        return Response(model_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#from apps.users.api.serializers import ModelExecution

### models_surveying
from models_surveying.surveying_models.surveying_model import SurveyingModel
from models_surveying.helpers import metrics_helper as Metrics

data_path = "users/files/df_mimic_mort_20210306_copy.csv"
test_result = "users/files/test_result/"
model_path = "users/new_model/SVC_Model_03092021202800"
_matrix_name = 'patientWardStayID'
_class_name = 'readmission'
_train_matrix_path = data_path
_result_path = test_result
_test_size = 0.20
_random_state = 123
_sampling_strategy = None
_features='cvp, etCo2, arterialLine, pa, ICP, temp_mean, temp_std, temp_autocorr, temp_slope, saO2_mean, saO2_std, saO2_autocorr, saO2_slope, heartRate_mean, heartRate_std, heartRate_autocorr, heartRate_slope, respiration_mean, respiration_std, respiration_autocorr, respiration_slope, etCo2_mean, etCo2_std, etCo2_autocorr, etCo2_slope, systolic_mean, systolic_std, systolic_autocorr, systolic_slope, bp_mean, bp_std, bp_autocorr, bp_slope, ptAge, African_American, Asian, Caucasian, Native_American, admissionHeigth, weigth, male'

@api_view(['POST'])
def surveying(request):
    ### Starting class
    surveying_model = SurveyingModel(
        model_path,
        _matrix_name,
        _features,
        _class_name,
        _train_matrix_path,
        _result_path,
        _test_size,
        _random_state,
        _sampling_strategy
    )

    ### Executing the classification
    result = surveying_model.Classify()

    return Response({'modelo ejecutado'},status = status.HTTP_200_OK)



@api_view(['POST'])
def graficas(request):
    title = 'Title ROC'
    save_path ='report/'
    fittedModelName='new_model/SVC_Model_04092021180745_fitted'

    x_train_path = 'result/train_features.csv'
    y_train_path = 'result/train_label.csv'
    x_test_path = 'result/test_features.csv'
    y_test_path = 'result/test_label.csv'
        
    model_path = fittedModelName

    factory = GraphFactory(x_train_path, y_train_path, x_test_path, y_test_path, model_path)
    factory.GenerateRocAucGraph(title, save_path)
    factory.GeneratePRCGraph("PCR plot", save_path)
    factory.GenerateSummaryGraph(save_path)





"""@api_view(['GET','POST'])
def execute_model(request):
    #list
    if request.method == 'GET':
        #queryset
        #users = User.objects.all()
        users_serializer=ModelExecution()
        return Response(users_serializer.data,status = status.HTTP_200_OK)

    #create
    elif request.method == 'POST':
        serializer = ModelExecution(data = request.data)
        if serializer.is_valid():

            

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""
      