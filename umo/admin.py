from django.contrib import admin

from umo import models

# Register your models here.

@admin.register(models.BRSpoints)
class AdminBRSpoints(admin.ModelAdmin):
    list_display = ['course', 'checkpoint', 'student', 'points']
    search_fields = ['student__FIO']
    list_filter = ['course']

admin.site.register(models.CheckPoint)
admin.site.register(models.Control)
admin.site.register(models.DisciplineDetails)
admin.site.register(models.EduOrg)
admin.site.register(models.EduPeriod)


@admin.register(models.Discipline)
class AdminDiscipline(admin.ModelAdmin):
    list_filter = ['program']
    search_fields = ['Name']


@admin.register(models.EduProgram)
class AdminEduProgram(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'profile', 'year', 'cathedra']
    search_fields = ['specialization__name']
    list_filter = ['cathedra']

admin.site.register(models.Exam)
admin.site.register(models.ExamMarks)


@admin.register(models.Group)
class AdminGroup(admin.ModelAdmin):
    list_display = ['Name', 'cathedra', 'program']
    search_fields = ['Name']
    list_filter = ['program']

@admin.register(models.GroupList)
class AdminGroupList(admin.ModelAdmin):
    list_display = ['group', 'student', 'active']
    search_fields = ['student__FIO']
    list_filter = ['group']
admin.site.register(models.Kafedra)
admin.site.register(models.Position)
admin.site.register(models.Profile)
admin.site.register(models.Semester)
admin.site.register(models.Specialization)
admin.site.register(models.Year)


@admin.register(models.Person)
class AdminPerson(admin.ModelAdmin):
    list_display = ('FIO', 'last_name', 'first_name', 'second_name')


@admin.register(models.Student)
class AdminStudent(admin.ModelAdmin):
    list_display = ('FIO', 'last_name', 'first_name', 'second_name')


@admin.register(models.Teacher)
class AdminTeacher(admin.ModelAdmin):
    list_display = ('FIO', 'last_name', 'first_name', 'second_name')


@admin.register(models.Course)
class AdminGroup(admin.ModelAdmin):
    list_display = ['discipline_detail', 'group', 'lecturer']
    search_fields = ['discipline_detail__discipline__Name']
    list_filter = ['group', 'lecturer']


admin.site.register(models.Synch)


@admin.register(models.CourseMaxPoints)
class CourseMaxPoints(admin.ModelAdmin):
    list_display = ['course', 'checkpoint', 'max_point']
    search_fields = ['course__discipline_detail__discipline__Name']
    list_filter = ['course__lecturer']
