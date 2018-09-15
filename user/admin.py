from django.contrib import admin

# Register your models here.
class U(admin.ModelAdmin):
        list_display = ('id','username',)  # list
from user import models
admin.site.register(models.User,U)
admin.site.register(models.Classroom)
admin.site.register(models.MeetingApplyStaus)
# admin.site.register(models.Order)
# admin.site.register(models.Detail)
# admin.site.register(models.Borrow)
admin.site.register(models.Schedule)
admin.site.register(models.Allowed_time)
admin.site.register(models.meetingApply)
# admin.site.register(models.Attendence)
