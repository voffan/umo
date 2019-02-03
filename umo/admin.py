from django.contrib import admin

from umo import models

# Register your models here.

admin.site.register(models.BRSpoints)
admin.site.register(models.CheckPoint)
admin.site.register(models.Control)
admin.site.register(models.Discipline)
admin.site.register(models.DisciplineDetails)
admin.site.register(models.EduOrg)
admin.site.register(models.EduPeriod)
admin.site.register(models.EduProgram)
admin.site.register(models.Exam)
admin.site.register(models.ExamMarks)


@admin.register(models.Group)
class AdminGroup(admin.ModelAdmin):
    list_display = ['Name', 'cathedra', 'program']
    search_fields = ['Name']
    list_filter = ['program']


admin.site.register(models.GroupList)
admin.site.register(models.Kafedra)
admin.site.register(models.Mark)
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
admin.site.register(models.CourseMaxPoints)
