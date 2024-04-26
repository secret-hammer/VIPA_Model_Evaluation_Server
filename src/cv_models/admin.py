from django.contrib import admin
from .models import Architecture, Task, Metric, Perspective, Environment \
    , TaskArchitectureRelationship, MetricPerspectiveTaskRelationship, Aspect

admin.site.register(Architecture)
admin.site.register(Task)
admin.site.register(Metric)
admin.site.register(Perspective)
admin.site.register(Environment)
admin.site.register(TaskArchitectureRelationship)
admin.site.register(MetricPerspectiveTaskRelationship)
admin.site.register(Aspect)
