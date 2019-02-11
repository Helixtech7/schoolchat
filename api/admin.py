from django.contrib import admin
from api import models

# Register your models here.
admin.site.register(models.ClassTable)
admin.site.register(models.Subject)
admin.site.register(models.Teacher)
admin.site.register(models.Student)
admin.site.register(models.Parent)
admin.site.register(models.ParentChild)
admin.site.register(models.TeacherClass)
admin.site.register(models.Assignment)
admin.site.register(models.AssignmentStudent)
admin.site.register(models.Notice)
admin.site.register(models.NoticeStudent)
admin.site.register(models.Activity)
admin.site.register(models.ActivityStudent)
admin.site.register(models.FeedbackStudent)
admin.site.register(models.Attendance)
admin.site.register(models.ReportCard)
