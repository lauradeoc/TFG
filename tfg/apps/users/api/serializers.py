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