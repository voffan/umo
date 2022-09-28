from django.contrib import admin

from rpd import models


# Register your models here.
admin.site.register(models.RPDDiscipline)
admin.site.register(models.Basement)
admin.site.register(models.DisciplineResult)
admin.site.register(models.RPDDisciplineContent)
admin.site.register(models.RPDDisciplineContentHours)
admin.site.register(models.ClassType)
admin.site.register(models.PracticeDescription)
admin.site.register(models.WorkType)
admin.site.register(models.DisciplineRating)
admin.site.register(models.MarkScale)
admin.site.register(models.FOS)
admin.site.register(models.ELibrary)
admin.site.register(models.Bibliography)
