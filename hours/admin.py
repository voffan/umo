from django.contrib import admin
from hours.models import (DisciplineSetting, GroupInfo, CourseHours, SupervisionHours, PracticeHours, OtherHours, CathedraEmployee)

admin.site.register(CourseHours)
admin.site.register(GroupInfo)
admin.site.register(DisciplineSetting)
admin.site.register(CathedraEmployee)
