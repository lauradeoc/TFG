from django.contrib import admin

from apps.users.models import User
from apps.users.models import MlrParams
from apps.users.models import MlrUserRol
from apps.users.models import MlrModel
from apps.users.models import MlrProject
from apps.users.models import MlrGraph
from apps.users.models import MlrResult
from apps.users.models import MrlProfile
from apps.users.models import MlrReport

admin.site.register(User)

admin.site.register(MlrParams)
admin.site.register(MlrUserRol)
admin.site.register(MlrModel)
admin.site.register(MlrProject)
admin.site.register(MlrGraph)
admin.site.register(MlrResult)
admin.site.register(MrlProfile)
admin.site.register(MlrReport)

# Register your models here.
