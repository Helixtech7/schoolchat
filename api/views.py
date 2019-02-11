from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User

import rest_framework.viewsets as viewset
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from rest_framework.parsers import MultiPartParser,FormParser
from firebase_admin import db
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound, ParseError
from rest_framework.parsers import MultiPartParser,FormParser, FileUploadParser
from .models import (ParentChild, Student, Assignment, Notice, NoticeStudent, AssignmentStudent,
                     TeacherClass, Activity, ActivityStudent, FeedbackStudent,ClassTable,Parent,
                     Teacher,Subject,Attendance,TeacherClass, Activity, ActivityStudent, FeedbackStudent,
                     ReportCard)
from PIL import Image
from .serializers import (CustomTokenObtainPairSerializer, ParentChildSerializer, StudentSerializer,
                          TeacherClassSerializer, NoticeSerializer, AssignmentSerializer, FeedbackStudentSerializer,
                          AttendanceSerializer, ActivitySerializer,
                          AssignmentStudentSerializer, NoticeStudentSerializer, ActivityStudentSerializer,
                          GetActivityStudentSerializer,GetAssignmentStudentSerializer,GetNoticeStudentSerializer,
                          ChildParentSerializer,ReportCardSeriazlier, FeedbackSerializer, UserSerializer)

from .serializers import (ClassTableSerializer,ParentSerializer,SubjectSerializer,
                          TeacherSerializer,NewParentChildSerializer,NewStudentSerializer,NewTeacherClassSerializer,
                          NewFeedbackStudentSerializer, StudentSerializerForTeacher)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Get Views
class ListClassesOfTeacher(APIView):
    """
    Return the list of classes in which a teacher teaches.
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, teacher_id, format=None):
        teacher = request.user.teacher
        if teacher.id != teacher_id:
            raise PermissionDenied(detail="Teacher is not same as user.")

        teacher_class = TeacherClass.objects.filter(teacher=teacher)
        serializer = TeacherClassSerializer(teacher_class, many=True)
        if serializer.data:
            response = serializer.data
            return Response(response)
        else:
            raise NotFound(detail='No records found')

class StudentListCreate(generics.ListAPIView):
    """
    APIView to get the list of students.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializerForTeacher
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        print(request.query_params)
        if 'class_id' in kwargs:
            return self._get_students_of_class(kwargs['class_id'])

        return super().get(request, *args, **kwargs)

    def _get_students_of_class(self, class_id):
        """
        :param class_id: id of ClassTable
        :return: Returns list of student belonging to particular class.
        """
        students = self.queryset.filter(class_id=class_id)
        serializer = StudentSerializerForTeacher(students,many=True)
        if serializer.data:
            response = serializer.data
            return Response(response)
        else:
            raise NotFound(detail="No records found")

class ListDetailsOfChild(APIView):
    """
    Return the Details of children of the parent
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        parent_child = ParentChild.objects.filter(parent=request.user.parent)
        parentchild = ParentChildSerializer(parent_child, many=True).data
        if parentchild:
            return Response(parentchild)
        else:
            raise NotFound(detail="No records found")

class ListParentDetailsOfChild(APIView):
    """
    Return the Details of children of the parent
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request,studentid, format=None):
        parent_child = ParentChild.objects.filter(child=studentid)
        parentchild = ChildParentSerializer(parent_child, many=True).data
        if parentchild:
            return Response(parentchild)
        else:
            raise NotFound(detail="No records found")

class ListAllAssignments(APIView):
    """
    Return the list of all assignments
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        assignment = Assignment.objects.all()
        response = AssignmentSerializer(assignment, many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")

class ListAllAssignmentsOfClass(APIView):
    """
    Return the list of all assignments of a class
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, classid, format = None):
        assignment = Assignment.objects.filter(teacher_class__class_id=classid)
        response = AssignmentSerializer(assignment, many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")

class ListAllAssignmentsForStudent(APIView):
    """
    Return the list of all assignments for a student
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request,studentid,format = None):
        assignment = AssignmentStudent.objects.filter(student=studentid)
        response = GetAssignmentStudentSerializer(assignment, many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")

class ListAllNotices(APIView):
    """
        Return the list of all notices
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        notice = Notice.objects.all()
        response = NoticeSerializer(notice, many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")

class ListAllNoticesOfClass(APIView):
    """
        Return the list of all notices of a particular class
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request,classid, format=None):
        notice = Notice.objects.filter(teacher_class__class_id = classid)
        # print(request.user.teacher.id)
        response = NoticeSerializer(notice, many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")


# class ListTeacherClass(APIView):
#     authentication_classes = (JWTAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     def get(self,request, id, format=None):
#         teacher_class = TeacherClass.objects.get(id=id)
#         if teacher_class is None:
#             raise NotFound(detail="not_found")
#         serializer = TeacherClassSerializerForTeacher(teacher_class)
#         return Response(serializer.data)


class ListAllNoticesForStudent(APIView):
    """
        Return the list of all notices for particular student
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, studentid, format=None):
        notice = NoticeStudent.objects.filter(student=studentid)
        # print(request.user.teacher.id)
        response = GetNoticeStudentSerializer(notice, many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")

class ListAllActivities(APIView):
    """
        Return the list of all activities
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request,format=None):
        activity = Activity.objects.all()
        # print(request.user.teacher.id)
        response = ActivitySerializer(activity, many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")


class ListAllActivitiesOfClass(APIView):
    """
        Return the list of all activities of particular class
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, classid, format=None):
        activity = Activity.objects.filter(teacher_class__class_id=classid)
        # print(request.user.teacher.id)
        response = ActivitySerializer(activity, many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")


class ListAllActivitiesForStudent(APIView):
    """
        Return the list of all activities for particular student
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, studentid, format=None):
        activity = ActivityStudent.objects.filter(student=studentid)
        # print(request.user.teacher.id)
        response = GetActivityStudentSerializer(activity, many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")


class FeedbackForParent(APIView):
    """
        get feedbacks for a child

    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request,studentid,format = None):
        s = FeedbackStudent.objects.filter(student=studentid)
        response = FeedbackStudentSerializer(s,many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")


class AllFeedback(APIView):
    """
         get all feedbacks

    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request,format=None):
        s = FeedbackStudent.objects.all()
        response = FeedbackStudentSerializer(s, many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")


class FeedbackForTeacher(APIView):
    """
        get feedbacks given by a particular teacher

    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, teacherid, format=None):
        if request.user.teacher.id != teacherid:
            raise PermissionDenied(detail="Teacher is not same as user")

        s = FeedbackStudent.objects.filter(teacher=teacherid)
        response = FeedbackStudentSerializer(s, many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")


class ListAllStudentsOfClass(APIView):
    """
        get list of students of a particular class
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request,classid):
        c = Student.objects.filter(class_id=classid)
        response = StudentSerializer(c,many=True).data
        if response:
            return Response(response)
        else:
            raise NotFound(detail="No records found")


def create_forgot_password_request(request, format=None):
    pass

# POST VIEWS


class PostAssignment(APIView):
    """
        add new assignment
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            students = request.data['students']
            assignment_student_data = []
            for i in students:
                data = {'assignment': serializer.data['id'], 'student': i}
                assignment_student_data.append(data)
            assignment_student_serializer = AssignmentStudentSerializer(data=assignment_student_data, many=True)
            if assignment_student_serializer.is_valid():
                assignment_student_serializer.save()
                return Response(serializer.data)
            else:
                activity = Assignment.objects.get(id=serializer.data['id'])
                activity.delete()
                raise ValidationError(detail="invalid_data", code=status.HTTP_400_BAD_REQUEST)


class PostActivity(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            students = request.data['students']
            activity_student_data = []
            for i in students:
                data = {'activity': serializer.data['id'], 'student': i}
                activity_student_data.append(data)
            activity_student_serializer = ActivityStudentSerializer(data=activity_student_data, many=True)
            if activity_student_serializer.is_valid():
                activity_student_serializer.save()
                return Response(serializer.data)
            else:
                activity = Activity.objects.get(id=serializer.data['id'])
                activity.delete()
                raise ValidationError(detail="invalid_data", code=status.HTTP_400_BAD_REQUEST)


class PostNotice(APIView):
    """
        add new notice
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = NoticeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            students = request.data['students']
            notice_student_data = []
            for i in students:
                data = {'notice': serializer.data['id'], 'student': i}
                notice_student_data.append(data)
            notice_student_serializer = NoticeStudentSerializer(data=notice_student_data, many=True)
            if notice_student_serializer.is_valid():
                notice_student_serializer.save()
                return Response(serializer.data)
            else:
                activity = Notice.objects.get(id=serializer.data['id'])
                activity.delete()
                raise ValidationError(detail="invalid_data", code=status.HTTP_400_BAD_REQUEST)


class PostFeedback(APIView):
    """
    add a new feedback
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)  # ,many=True
        if serializer.is_valid(raise_exception=ValidationError):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostAttendance(APIView):
    """
    add a new Attendance
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceView(APIView):
    """
    Get attendance of student
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request,student_id):
        try:
            attendance = Attendance.objects.filter(student__id=student_id)
            serializer = AttendanceSerializer(attendance, many=True)
            return Response(serializer.data)
        except Attendance.DoesNotExist:
            raise NotFound(detail="not_found")
        except ValidationError:
            raise

class ReportView(APIView):
    """
    ReportView for posting and getting list for a student
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request,student_id):
        try:
            report_cards = ReportCard.objects.filter(student__id=student_id)
            serializer = ReportCardSeriazlier(report_cards,many=True)
            return Response(serializer.data)
        except ReportCard.DoesNotExist:
            raise NotFound(detail="not_found")

    def post(self, request):
        serializer = ReportCardSeriazlier(data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def put(self, request, data_type, id, format=None):
        print(request.data)
        if 'file' not in request.data:
            raise ParseError("empty_content")

        f = request.data['file']
        try:
            image = Image.open(f)
            image.verify()

        except:
            raise ParseError("unsupported_image_type")
        if data_type == 'activity':
            activity = Activity.objects.get(id=id)
            activity.image = f
            activity.save()
            activity_serializer = ActivitySerializer(activity)
            return Response(activity_serializer.data)
        elif data_type == 'notice':
            notice = Notice.objects.get(id=id)
            notice.image = f
            notice.save()
            notice_serializer = NoticeSerializer(notice)
            return Response(notice_serializer.data)
        elif data_type == "assignment":
            assignment = Assignment.objects.get(id=id)
            assignment.image = f
            assignment.save()
            assignment_serializer = AssignmentSerializer(assignment)
            return Response(assignment_serializer.data)
        elif data_type == "report_card":
            report_card = ReportCard.objects.get(id=id)
            report_card.image = f
            report_card.save()
            report_card_serializer = ReportCardSeriazlier(report_card)
            return Response(report_card_serializer.data)
        else:
            raise ValidationError(detail="invalid_data_type")



#PUT VIEWs
class UpdateChildProfile(APIView):
    """
    update child profile given his/her id

    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    def put(self, request, studentid):
        s = Student.objects.get(pk=studentid)
        serializer = StudentSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAssignment(APIView):
    """
    Update assignment
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, id):
        assignment = Assignment.objects.get(id=id)
        serializer = AssignmentSerializer(assignment, data=request.data)
        if serializer.is_valid(ValidationError):
            if 'students' not in request.data:
                raise ValidationError
            AssignmentStudent.objects.all().filter(assignment=assignment).delete()
            serializer.save()
            for student in Student.objects.filter(id__in=request.data['students']):
                x = AssignmentStudent()
                x.assignment = assignment
                x.student=student
                x.save()
            return Response({"success": True, "message": "OK"})

    def delete(self, request, id):
        try:
            assignment = Assignment.objects.get(id=id)
            assignment.delete()
        except Assignment.DoesNotExist:
            raise NotFound(detail="not_found")
        return Response({"success": True, "message": "OK"})


class UpdateActivity(APIView):
    """
    Update Activity
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, id):
        activity = Activity.objects.get(id=id)
        serializer = ActivitySerializer(activity,data=request.data)
        if serializer.is_valid(ValidationError):
            if 'students' not in request.data:
                raise ValidationError
            ActivityStudent.objects.all().filter(activity=activity).delete()
            serializer.save()
            for student in Student.objects.filter(id__in=request.data['students']):
                x = ActivityStudent()
                x.activity = activity
                x.student=student
                x.save()
            return Response({"success": True, "message": "OK"})

    def delete(self, request, id):
        try:
            activity = Activity.objects.get(id=id)
            activity.delete()
        except Activity.DoesNotExist:
            raise NotFound(detail="not_found")
        return Response({"success": True, "message": "OK"})


class UpdateNotice(APIView):
    """
    Update and delete notice
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, id):
        notice = Notice.objects.get(id=id)
        serializer = NoticeSerializer(notice,data=request.data)
        if serializer.is_valid(ValidationError):
            if 'students' not in request.data:
                raise ValidationError
            NoticeStudent.objects.all().filter(notice=notice).delete()
            serializer.save()
            for student in Student.objects.filter(id__in=request.data['students']):
                x = NoticeStudent()
                x.notice = notice
                x.student = student
                x.save()
            return Response({"success": True, "message": "OK"})

    def delete(self,request,id):
        try:
            notice = Notice.objects.get(id=id)
            notice.delete()
        except Notice.DoesNotExist:
            raise NotFound(detail="not_found")
        return Response({"success": True, "message": "OK"})



# FOR ADMIN

class ClassTableList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    parser_classes = (MultiPartParser, FormParser)

    queryset = ClassTable.objects.all()
    serializer_class = ClassTableSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = ClassTable.objects.get(pk=pk)
        serializer = ClassTableSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    parser_classes = (MultiPartParser, FormParser)

    queryset = Student.objects.all()
    serializer_class = NewStudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = Student.objects.get(pk=pk)
        serializer = NewStudentSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ParentList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = Parent.objects.get(pk=pk)
        serializer = ParentSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ParentChildList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    queryset = ParentChild.objects.all()
    serializer_class = NewParentChildSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = ParentChild.objects.get(pk=pk)
        serializer = NewParentChildSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)

class TeacherList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    parser_classes = (MultiPartParser, FormParser)

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = Teacher.objects.get(pk=pk)
        serializer = TeacherSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubjectList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = Subject.objects.get(pk=pk)
        serializer = SubjectSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TeacherClassList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    queryset = TeacherClass.objects.all()
    serializer_class = NewTeacherClassSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, pk):
        s = TeacherClass.objects.get(pk=pk)
        serializer = NewTeacherClassSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivityList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    parser_classes = (MultiPartParser, FormParser)

    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = Activity.objects.get(pk=pk)
        serializer = ActivitySerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ActivityStudentList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    queryset = ActivityStudent.objects.all()
    serializer_class = ActivityStudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, pk):
        s = ActivityStudent.objects.get(pk=pk)
        serializer = ActivityStudentSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AssignmentList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    parser_classes = (MultiPartParser, FormParser)

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = Assignment.objects.get(pk=pk)
        serializer = AssignmentSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AssignmentStudentList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    queryset = AssignmentStudent.objects.all()
    serializer_class = AssignmentStudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = AssignmentStudent.objects.get(pk=pk)
        serializer = AssignmentStudentSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class NoticeList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    parser_classes = (MultiPartParser, FormParser)

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = Notice.objects.get(pk=pk)
        serializer = NoticeSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class NoticeStudentList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    queryset = NoticeStudent.objects.all()
    serializer_class = NoticeStudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = NoticeStudent.objects.get(pk=pk)
        serializer = NoticeStudentSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AttendanceList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def put(self, request, pk):
        s = Attendance.objects.get(pk=pk)
        serializer = AttendanceSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FeedbackStudentList(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    queryset = FeedbackStudent.objects.all()
    serializer_class = NewFeedbackStudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, pk):
        s = FeedbackStudent.objects.get(pk=pk)
        serializer = NewFeedbackStudentSerializer(s, data=request.data)  # ,many=True
        if serializer.is_valid(ValidationError):
            serializer.save()
            return Response({"success": True, "message": "OK"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, *args, **kwargs):
        temp = self.get_object()
        if temp:
            temp.delete()
            return Response({"success": True, "message": "OK"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SyncUsersToFirebase(APIView):
    # authentication_classes = (JWTAuthentication,)
    # permission_classes = (IsAdminUser,)

    def get(self,request):
        ref = db.reference('Users')
        users = {}
        for user in User.objects.all():
            users[user.id] = {
                'id': user.id,
                'parent': False,
                'teacher': False,
                'username': user.username,
                'status': 'offline',
                'search': None,
                'imageURL': 'default'
            }
            if hasattr(user,'parent'):
                parent = user.parent
                users[user.id]['parent'] = True
                users[user.id]['search'] = parent.first_name + ' ' + parent.surname
            if hasattr(user, 'teacher'):
                teacher = user.teacher
                users[user.id]['teacher'] = True
                users[user.id]['search'] = teacher.first_name + ' ' + teacher.surname
                users[user.id]['imageURL'] = teacher.image.url
        ref.set(users)
        return Response(users)


class UserViewSet(viewset.ModelViewSet):
    """
    Viewset for User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)