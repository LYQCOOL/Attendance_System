from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)
    realname=models.CharField(max_length=32)
    email=models.EmailField()
    phone=models.CharField(max_length=12)

# class Attendence(models.Model):
#     #签到表   字段：用户，签到时间，签退时间，描述   其他是为了方便操作加的字段可不写
#     stu = models.ForeignKey(to='User',on_delete=True)
#     # cur_time = models.DateTimeField(auto_now_add=True)
#     start_time = models.DateTimeField(null=True, blank=True)
#     end_time = models.DateTimeField(null=True, blank=True)
#     # type_choice=(
#     #     (1,'8:00'),
#     #     (2,'9:00'),
#     #     (3,'10:00'),
#     #     (4,'11:00'),
#     #     (5,'12:00'),
#     #     (6,'13:00'),
#     #     (7,'14:00'),
#     #     (8,'15:00'),
#     #     (9,'16:00'),
#     #     (10,'17:00'),
#     #     (11,'18:00'),
#     #     (12,'19:00'),
#     #     (13,'20:00'),
#     #     (14,'21:00'),
#     #     (15,'22:00'),
#     # )
#     # start_time=models.IntegerField(choices=type_choice)
#     # end_time=models.IntegerField(choices=type_choice)
#     duration = models.DecimalField(max_digits=5, decimal_places=2, default=0)
#     date = models.DateField(default=timezone.now)
#     # state=models.BooleanField(default=False)
#     is_leave = models.BooleanField(default=False)
#     detail = models.TextField(default='无')
#     leave_count = models.IntegerField(default=0)
class Classroom_status(models.Model):
    statu=models.CharField(max_length=32)
class Classroom(models.Model):
    location=models.CharField(max_length=32)
    space=models.IntegerField()
    introduction=models.CharField(max_length=32,null=True)
    status=models.ForeignKey(Classroom_status,on_delete=True)
    remark=models.CharField(max_length=32,null=True)
class Allowed_time(models.Model):
    a_time=models.TimeField()
class Schedule(models.Model):
    img = models.ImageField(upload_to='image')
    location=models.ForeignKey(Classroom,on_delete=True)
    begintime=models.DateTimeField()
    endtime=models.DateTimeField()
    day=models.DateField()
    # type_choice=(
    #     (1,'8:00'),
    #     (2,'9:00'),
    #     (3,'10:00'),
    #     (4,'11:00'),
    #     (5,'12:00'),
    #     (6,'13:00'),
    #     (7,'14:00'),
    #     (8,'15:00'),
    #     (9,'16:00'),
    #     (10,'17:00'),
    #     (11,'18:00'),
    #     (12,'19:00'),
    #     (13,'20:00'),
    #     (14,'21:00'),
    #     (15,'22:00'),
    # )
    # begintime=models.IntegerField(choices=type_choice)
    # endtime=models.IntegerField(choices=type_choice)
# class Classopentime(models.Model):
#     classname=models.ForeignKey(to='Classroom',to_field='id',on_delete=True)
#     startime=models.DateTimeField()
#     endtime=models.DateTimeField()

# class Borrow(models.Model):
#     user=models.ForeignKey(to='User',to_field='id',on_delete=True)
#     room=models.ForeignKey(to='Classroom',to_field='id',on_delete=True)
#     # operate_time=models.DateTimeField()
#     starttime=models.DateTimeField()
#     endtime=models.DateTimeField()

# class ConfeRoom(models.Model):
#         num = models.CharField(max_length=5)
#         name = models.CharField(max_length=50)
#         size = models.CharField(max_length=5)
#         acad = models.CharField(max_length=30)
#
#         class MEAT:  # 引入MEAT中间件，为了在前端显示的时候以“num”顺序排列，与下一个类似
#             ordering = ["num"]
#
#         def __unicode__(self):
#             return self.num
#             # 会议室详情

# class Detail(models.Model):
#         name = models.CharField(max_length=50)
#         img = models.ImageField(upload_to="image")  # 图片类型，参数表示上传图片
#         time = models.CharField(max_length=20)
#         room = models.ForeignKey(ConfeRoom,on_delete=True)  # 这里采用多对一的关系，一个学院有很多会议室，而一个会议室只能属于一个学院
#
#         class MEAT:
#             ordering = ["name"]
#
#         def __unicode__(self):
#             return self.name

    # 订单信息
# class Order(models.Model):
#         user = models.CharField(max_length=30)
#         num = models.CharField(max_length=10)
#         name = models.CharField(max_length=50)
#         time = models.CharField(max_length=20)
#         size = models.CharField(max_length=5)
#         phone = models.CharField(max_length=11)
#         ntime = models.CharField(max_length=30)
#
#         def __unicode__(self):
#             return self.user
class MeetingApplyStaus(models.Model):
    statusName=models.CharField(max_length=32)

class meetingApply(models.Model):
    workerID=models.ForeignKey(User,on_delete=True)
    topic=models.CharField(max_length=32)
    homeID=models.ForeignKey(Classroom,on_delete=True)
    attendance=models.IntegerField()
    beginTime=models.TimeField()
    endTime=models.TimeField()
    day=models.DateField()
    statusID=models.ForeignKey(MeetingApplyStaus,on_delete=True)
    applytime=models.DateTimeField(auto_now_add=True)







