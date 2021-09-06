from django.db.models import fields
from rest_framework import serializers
from apps.users.models import User
from apps.users.models import MlrGraph
from apps.users.models import MlrModel
from apps.users.models import MlrParams
from apps.users.models import MrlProfile
from apps.users.models import MlrProject
from apps.users.models import MlrReport
from apps.users.models import MlrResult
from apps.users.models import MlrModel

# USUARIO
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= '__all__'

    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self,instance,validated_data):
        updated_user=super().update(instance,validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user

"""class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'password': instance['password']
        }"""

# GRAFICAS

class GraphSerializer(serializers.ModelSerializer):

    class Meta:
        model = MlrGraph
        fields = ('id', 'title', 'save_path', 'mlr_model')

# MODELOS

class ModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MlrModel
        read_only_fields = (
            'id',
            #'model_name',
            'created_at',
            'created_by',
        )
        fields = ('id',
                  'model_name',
                  'new_model_file_path',
                  'fitted_model_file_path',
                  'params',
                  'created_at',
                  'updated_at',
                  "created_by"
                  )

# PARAMETROS
class ParamSerializer(serializers.ModelSerializer):

    class Meta:
        model = MlrParams
        fields = ('id', 'name', 'value', 'mlr_model')

# PERFIL

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = MrlProfile
        fields = ('id', 'bio', 'web', 'user_id ')

# PROYECTO - MODELO
class ProjectModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MlrProject
        fields = ('id',
                  'mlrproject_id',
                  'mlrmodel_id')

# PROYECTO


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = MlrProject
        read_only_fields = (
            'id',
            'created_at',
            'created_by',
        )
        fields='__all__'
        """fields = ('id',
                  'name',
                  'file_data',
                  'matrix_name',
                  'attrs_name',
                  'class_name',
                  'test_size ',
                  'random_state ',
                  'sampling_strategy ',
                  'x_train_path',
                  'y_train_path',
                  'x_test_path',
                  'y_test_path',
                  'created_at',
                  'updated_at',
                  'created_by',
                )"""

# REPORTES

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = MlrReport
        fields = ('id',
                  'name',
                  'type',
                  'path',
                  'created',
                  'updated',
                  'mlr_model')

# RESULTADOS


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = MlrResult
        fields = ('id',
                  'name',
                  'value',
                  'type',
                  'mlr_report')


class UserRolSerializer(serializers.ModelSerializer):

    class Meta:
        model = MlrModel
        fields = ('id', 'name', 'type_user')


SAMPLING_STRATEGY_CHOICES = (
    ('NONE', None),
)

class ExecutionSerializer(serializers.Serializer):
    model_path=serializers.CharField(max_length=300)
    _matrix_name=serializers.CharField(max_length=100)
    _class_name=serializers.CharField(max_length=100)
    _train_matrix_path=serializers.CharField(max_length=100)
    _result_path=serializers.CharField(max_length=100)
    _test_size=serializers.FloatField()
    _random_state=serializers.IntegerField()
    #_sampling_strategy=serializers.ChoiceField(choices=SAMPLING_STRATEGY_CHOICES)
    _sampling_strategy=serializers.CharField(default=None)
    _features=serializers.CharField(max_length=900)



KERNEL_CHOICES =( 
    ("","-------------"),  
    ("linear", "linear"),
    ("poly", "poly"),
    ("rbf", "rbf"),
    ("sigmoid", "sigmoid"),
    ("precomputed", "precomputed"),
)
class MlrSVCModel(serializers.Serializer):
    model_name = serializers.CharField(required=True,initial='SVC')
    new_model_file_path = serializers.CharField(max_length=500)
    fitted_model_file_path = serializers.CharField(max_length=500)
    c=serializers.FloatField()
    kernel=serializers.ChoiceField(label="kernel",required=False,choices=KERNEL_CHOICES)
    degree=serializers.IntegerField(label="degree",required=False)
    random_state=serializers.IntegerField(label="random_state",required=False)
    #created_at = serializers.DateTimeField(auto_now_add=True)
    #updated_at = serializers.DateTimeField(auto_now_add=True)
    #created_by = serializers.ForeignKey(User, on_delete=serializers.CASCADE)

