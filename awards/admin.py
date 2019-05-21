from django.contrib import admin

# Register your models here.
from awards import models


admin.site.register(models.Award)
admin.site.register(models.EmployeeAward)
admin.site.register(models.Issuer)
admin.site.register(models.AwardType)