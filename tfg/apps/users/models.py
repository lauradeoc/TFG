from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model

MODEL_CHOICES = (
    ('SVC', 'SVC'),
    ('DT', 'DT'),
    ('XGBOOST', 'XGBOOST'),
    ('RF', 'RF'),
    ('NNC', 'NNC'),
)

REPORT_CHOICES = (
    ('CSV', 'csv'),
    ('TXT', 'txt'),
)

RESULT_CHOICES = (
    ('TEST', 'test'),
    ('TRAIN', 'train'),
)

SAMPLING_STRATEGY_CHOICES = (
    ('NONE', None),
)

class UserManager(BaseUserManager):
    def _create_user(self, username, email, name,last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, name,last_name, password=None, **extra_fields):
        return self._create_user(username, email, name,last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name,last_name, password=None, **extra_fields):
        return self._create_user(username, email, name,last_name, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 255, unique = True)
    email = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    name = models.CharField('Nombres', max_length = 255, blank = True, null = True)
    last_name = models.CharField('Apellidos', max_length = 255, blank = True, null = True)
    image = models.ImageField('Imagen de perfil', upload_to='perfil/', max_length=255, null=True, blank = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','name','last_name']

    def __str__(self):
        return f'{self.name} {self.last_name}'


# ROLES
class MlrUserRol(models.Model):
    name = models.CharField(max_length=50)
    type_user = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roles'

    def __str__(self):
        return self.name

class MrlProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True)
    web = models.URLField(blank=True)

    rol = models.ManyToManyField(MlrUserRol)

    def __str__(self):
        return self.user.username


User = get_user_model()

class MlrModel(models.Model):
    model_name = models.CharField(max_length=50, choices=MODEL_CHOICES)
    new_model_file_path = models.CharField(max_length=500)
    fitted_model_file_path = models.CharField(max_length=500)
    params=models.CharField(max_length=2000,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['model_name']
        verbose_name = 'model'
        verbose_name_plural = 'models'

    def __str__(self):
        return self.model_name


        

# PARAMETROS
class MlrParams(models.Model):

    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30,null=True,blank=True)
    mlr_model = models.ForeignKey(MlrModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = 'mlr_param'
        verbose_name_plural = 'mlr_params'

    def __str__(self):
        return self.name

class MlrGraph(models.Model):
    title = models.CharField(max_length=100)
    save_path = models.CharField(max_length=1000)

    mlr_model = models.ForeignKey(MlrModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']

# PROYECTOS
class MlrProject(models.Model):
    name = models.CharField(max_length=50)
    file_data = models.FileField(upload_to='users/files/%Y/%m/%d/', null=True, blank=True)
    matrix_name = models.CharField(max_length=50)
    attrs_name = models.CharField(max_length=3000)
    class_name = models.CharField(max_length=50)
    test_size = models.FloatField()
    random_state = models.DecimalField(max_digits=5, decimal_places=0)
    sampling_strategy = models.CharField(max_length=20, choices=SAMPLING_STRATEGY_CHOICES)

    x_train_path = models.CharField(max_length=500)
    y_train_path = models.CharField(max_length=500)
    x_test_path = models.CharField(max_length=500)
    y_test_path = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    mlr_model = models.ManyToManyField(MlrModel)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    def __str__(self):
        return self.name

# REPORTES
class MlrReport(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=50, choices=REPORT_CHOICES)
    path = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    mlr_model = models.ForeignKey(MlrModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

# RESULTADOS
from django.db import models

class MlrResult(models.Model):
    name = models.CharField(max_length=30)
    value = models.FloatField()
    type = models.CharField(max_length=50, choices=RESULT_CHOICES)
    mlr_report = models.ForeignKey(MlrReport, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']



"""class ModelExecution(models.Model):
    model_path=models.CharField(max_length=300)
    _matrix_name=models.CharField(max_length=100)
    _class_name=models.CharField(max_length=100)
    _train_matrix_path=models.CharField(max_length=100)
    _result_path=models.CharField(max_length=100)
    _test_size=models.FloatField()
    _random_state=models.IntegerField()
    _sampling_strategy=models.CharField(max_length=100)
    _features=models.CharField(max_length=100)"""