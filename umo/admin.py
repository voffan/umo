from django.contrib import admin

from umo import models

# Register your models here.

admin.site.register(models.BRSpoints)
admin.site.register(models.CheckPoint)
admin.site.register(models.Control)
admin.site.register(models.ControlType)
admin.site.register(models.Discipline)
admin.site.register(models.DisciplineDetails)
admin.site.register(models.EduOrg)
admin.site.register(models.EduPeriod)
admin.site.register(models.EduProg)
admin.site.register(models.Exam)
admin.site.register(models.ExamMarks)


@admin.register(models.Group)
class AdminGroup(admin.ModelAdmin):
    list_display = ['Name', 'cathedra', 'program']
    search_fields = ['Name']
    list_filter = ['program']


admin.site.register(models.GroupList)
admin.site.register(models.Kafedra)
admin.site.register(models.Level)
admin.site.register(models.Mark)
admin.site.register(models.MarkSymbol)
admin.site.register(models.Person)
admin.site.register(models.Position)
admin.site.register(models.Profile)
admin.site.register(models.Qual)
admin.site.register(models.Semestr)
admin.site.register(models.Specialization)
admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Year)
admin.site.register(models.Zvanie)


@admin.register(models.Course)
class AdminGroup(admin.ModelAdmin):
    list_display = ['discipline_detail', 'group', 'lecturer']
    search_fields = ['discipline_detail__discipline__Name']
    list_filter = ['group', 'lecturer']


admin.site.register(models.Synch)