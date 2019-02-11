from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .models import (ParentChild, Student, Activity, Attendance,
                     ActivityStudent, AssignmentStudent, NoticeStudent,
                     ClassTable, TeacherClass, Assignment, Notice,
                     FeedbackStudent,Parent,Teacher,Subject, ReportCard)
from django.contrib.auth.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    _TEACHER_TYPE = 'type_teacher'
    _PARENT_TYPE = 'type_parent'

    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        user_type = {
            'teacher': False,
            'parent': False,
            'teacher_id': -1,
            'parent_id': -1
        }

        if hasattr(user, 'teacher'):
            user_type['teacher'] = True
            user_type['teacher_id'] = user.teacher.id
        if hasattr(user, 'parent'):
            user_type['parent'] = True
            user_type['parent_id'] = user.parent.id

        token['user_type'] = user_type
        return token


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class NewTeacherClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherClass
        fields = "__all__"

class ClassTableSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = ClassTable
        fields = "__all__"

class NewStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"


class NewParentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentChild
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"


class NewFeedbackStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackStudent
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"


class ActivityStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityStudent
        fields = "__all__"

class AssignmentStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentStudent
        fields = "__all__"

class NoticeStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeStudent
        fields = "__all__"


class ClassSerializer(serializers.ModelSerializer):
    """
    Serializer for class table
    """
    image = serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = ClassTable
        fields = ('id', 'class_name', 'class_teacher')
        depth = 1


class TeacherClassSerializer(serializers.ModelSerializer):
    """
    Serializer for TeacherClass table
    """
    class Meta:
        model = TeacherClass
        depth = 1
        fields = '__all__'


# class TeacherClassSerializerForTeacher(serializers.ModelSerializer):
#     """
#     TeacherClass serializer
#     """
#     class Meta:
#         model = TeacherClass
#         fields = '__all__'

class ParentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentChild
        fields = ('id','child')
        depth = 2

class GetActivityStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityStudent
        fields = ('activity',)
        depth = 3

class GetAssignmentStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentStudent
        fields = ('assignment',)
        depth = 3

class GetNoticeStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeStudent
        fields = ('notice',)
        depth = 3

class ChildParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentChild
        fields = ('relation','parent')
        depth = 1

class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student table
    """
    image = serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = Student
        fields = '__all__'
        depth = 1

class StudentSerializerForTeacher(serializers.ModelSerializer):
    """
    Serializer for Student table
    """
    image = serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = Student
        fields = '__all__'

class FeedbackStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackStudent
        fields = "__all__"
        depth = 1

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackStudent
        fields = '__all__'

class ReportCardSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = ReportCard
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

