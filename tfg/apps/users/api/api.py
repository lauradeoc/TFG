from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from apps.users.models import User
from apps.users.api.serializers import UserSerializer
from rest_framework import viewsets

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

class MlrGraphViewSet(viewsets.ModelViewSet):
    serializer_class = GraphSerializer
    queryset = MlrGraph.objects.all()

    def perform_create(self, serializer):
        #serializer.save(created_by=self.request.user)
        serializer.save()

    def get_queryset(self):
        #return self.queryset.filter(created_by=self.request.user)
        return self.queryset

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



from apps.users.models import MlrModel
from apps.users.api.serializers import ModelSerializer

class MlrModelViewSet(viewsets.ModelViewSet):
    serializer_class = ModelSerializer
    queryset = MlrModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


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
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        return Response(status=status.HTTP_204_NO_CONTENT)"""


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

class MlrReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = MlrReport.objects.all()

    def perform_create(self, serializer):
        #serializer.save(created_by=self.request.user)
        serializer.save()

    def get_queryset(self):
        #return self.queryset.filter(created_by=self.request.user)
        return self.queryset

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