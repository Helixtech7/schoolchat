from django.db import models
import datetime
from django.contrib.auth.models import User
import os
# Create your models here.

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('T', 'Transgender'),
)


UNKNOWN = 'U'
BLOOD_GROUP_CHOICES = (
    ('O+ve',' O positive'),
    ('O-ve', 'O negative'),
    ('A+ve', 'A positive'),
    ('A-ve', 'A negative'),
    ('B+ve', 'B positive'),
    ('B-ve', 'B negative'),
    ('AB+ve', 'O positive'),
    ('AB-ve', 'O negative'),
    ('U', 'Unknown')
)

PARENT_CHILD_RELATION_CHOICES = (
    ('M','Mother'),
    ('F', 'Father'),
    ('G', 'Guardian')
)
ATTENDANCE_CHOICE =(
    ('P','Present'),
    ('A','Absent')
)

class ClassTable(models.Model):
    class_name = models.CharField(max_length=32, null=False)
    class_teacher = models.OneToOneField('Teacher', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='classtables/', default='classtables/none/timetable.png')

    def __str__(self):
        return 'Class: ' + self.class_name

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        ordering = ('class_name',)


class Student(models.Model):
    enrollment_no = models.CharField(max_length=10,default='')
    roll_no = models.CharField(max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255)

    class_id = models.ForeignKey(ClassTable, on_delete=models.SET_NULL, blank=False, null=True)
    dob = models.DateField(default=datetime.date.today)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True, max_length=1)
    blood_group = models.CharField(choices=BLOOD_GROUP_CHOICES, default=UNKNOWN, max_length=4)
    height = models.FloatField(blank=True, null=True,help_text="in cm")
    weight = models.FloatField(blank=True, null=True,help_text="in kg")
    address_line_1 = models.TextField(max_length=255, blank=True, null=True)
    address_line_2 = models.TextField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    district = models.CharField(max_length=32, blank=True, null=True)
    state = models.CharField(max_length=32, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    pin_code = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='students/',default='students/none/no_image.jpg')

    def __str__(self):
        return self.first_name + ' ' + self.surname + " -- " + str(self.class_id)

    class Meta:
        ordering = ('class_id', 'roll_no')


class Parent(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255)
    residential_address = models.TextField(max_length=255)
    primary_contact = models.CharField(max_length=13)
    secondary_contact = models.CharField(blank=True, null=True,max_length=13)
    occupation = models.CharField(max_length=50,blank=True, null=True)
    office_address = models.TextField(max_length=255,blank=True, null=True)
    office_no = models.CharField(blank=True, null=True, max_length=13)
    email_id = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.surname

    class Meta:
        ordering = ('first_name', 'surname')


class ParentChild(models.Model):
    parent = models.ForeignKey(Parent,on_delete=models.CASCADE)
    child = models.ForeignKey(Student, on_delete=models.CASCADE)
    relation = models.CharField(choices=PARENT_CHILD_RELATION_CHOICES, max_length=1)

    class Meta:
        verbose_name = 'Parent Child Relationship'
        verbose_name_plural = 'Parent Child Relationships'
        ordering = ('child',)

    def __str__(self):
        return "Parent: " + str(self.parent) + " Child: " + str(self.child)


class Teacher(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=13)
    email_id = models.EmailField()
    image = models.ImageField(upload_to='teachers/', default='teachers/none/teacher.jpg')

    def __str__(self):
        return self.first_name + ' ' + self.surname

    class Meta:
        ordering = ('first_name', 'surname')


class Subject(models.Model):
    subject_name = models.CharField(max_length=32)

    def __str__(self):
        return self.subject_name

    class Meta:
        ordering = ('subject_name',)


class TeacherClass(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id = models.ForeignKey(ClassTable, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.class_id) + " " + str(self.teacher) + "-" + str(self.subject)

    class Meta:
        verbose_name = 'Teacher Class Relationship'
        verbose_name_plural = 'Teacher Class Relationships'
        ordering = ('class_id',)


class PasswordResetRequest(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    temporary_password = models.CharField(max_length=5)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_through = models.DateTimeField()

    class Meta:
        ordering = ('-valid_from',)


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    teacher_class = models.ForeignKey(to=TeacherClass, on_delete=models.SET_NULL, null=True, blank=True)
    ## class_id = models.ForeignKey(ClassTable,on_delete=models.CASCADE)
    ## teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    ## subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='assignments/', default='assignments/none/assignment.jpg')
    date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return "Title :" + self.title + " -- " + str(self.teacher_class)

    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        #ordering = ('title','teacher_class',)
        ordering = ('-date',)

class AssignmentStudent(models.Model):
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.assignment) + " -- " + str(self.student)

    class Meta:
        verbose_name = 'Assignment Student'
        # verbose_name_plural = ''
        ordering = ('assignment',)


class Notice(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    teacher_class = models.ForeignKey(to=TeacherClass, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='notices/', default='notices/none/notice.png')
   ## class_id = models.ForeignKey(ClassTable, on_delete=models.CASCADE)
    ## teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Title :" + self.title + " -- " + str(self.teacher_class)

    class Meta:
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'
        # ordering = ('title', 'teacher_class',)
        ordering = ('-date',)


class NoticeStudent(models.Model):
    notice = models.ForeignKey(Notice,on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return "Notice : " + str(self.notice) + " -- " + str(self.student)

    class Meta:
        verbose_name = 'Notice Student'
        # verbose_name_plural = ''
        ordering = ('notice',)


class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    teacher_class = models.ForeignKey(to=TeacherClass, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='activities/', default='activities/none/activity.png')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Title :" + self.title + " -- " + str(self.teacher_class)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        # ordering = ('title','teacher_class',)
        ordering = ('-date',)


class ActivityStudent(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return "Activity : " + str(self.activity)

    class Meta:
        verbose_name = 'Activity Student'
        # verbose_name_plural = ''
        ordering = ('activity',)


class FeedbackStudent(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Teacher : " + str(self.teacher) + " Student : " + str(self.student)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        # ordering = ('feedback', 'teacher',)
        ordering = ('-date',)


class Attendance(models.Model):
    teacher_class = models.ForeignKey(TeacherClass, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    total_days_present = models.IntegerField(default=0)
    total_days_absent = models.IntegerField(default=0)

    def __str__(self):
        return "Student : " + str(self.student)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        # ordering = ('student', 'attendance')
        ordering = ('-date',)


class ReportCard(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    teacher_class = models.ForeignKey(TeacherClass, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='report/', null=True, blank=True)
    remarks = models.CharField(max_length=255)

    def __str__(self):
        return "Title: " + self.title + " Student: " + str(self.student)

    class Meta:
        verbose_name = 'Report Card'
        verbose_name_plural = 'Report Cards'
        ordering = ('-date',)
