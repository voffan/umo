from django.contrib import admin
from .models import Group, GroupList, Student, Person, Teacher, Kafedra, Year, EduProg, EduOrg, Specialization, Profile, Qual, Level
# Register your models here.

admin.site.register(Group)
admin.site.register(GroupList)
admin.site.register(Student)
admin.site.register(Person)
admin.site.register(Teacher)
admin.site.register(Kafedra)
admin.site.register(Year)
admin.site.register(EduProg)
admin.site.register(EduOrg)
admin.site.register(Specialization)
admin.site.register(Profile)
admin.site.register(Qual)
admin.site.register(Level)