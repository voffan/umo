from django.contrib import admin
from hours.models import (DisciplineSetting, GroupInfo, CourseHours, SupervisionHours, PracticeHours, OtherHours, CathedraEmployee, HoursSettings, NormControl, TeacherGekStatus, StudentsGroup)

admin.site.register(CourseHours)
admin.site.register(GroupInfo)
admin.site.register(DisciplineSetting)
admin.site.register(CathedraEmployee)
admin.site.register(SupervisionHours)
admin.site.register(PracticeHours)
admin.site.register(OtherHours)
admin.site.register(HoursSettings)
admin.site.register(NormControl)
admin.site.register(TeacherGekStatus)
admin.site.register(StudentsGroup)
