from django.contrib import admin
from .models import Architecture, Task, Metric, Perspective, Environment,  Aspect, Parameter

admin.site.register(Architecture)
admin.site.register(Parameter)
admin.site.register(Task)
admin.site.register(Metric)
admin.site.register(Perspective)
admin.site.register(Environment)
admin.site.register(Aspect)
