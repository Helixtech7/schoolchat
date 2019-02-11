from django.contrib import admin
from . import views

from django.urls import path, include
from .views import (CustomTokenObtainPairView, ListClassesOfTeacher, StudentListCreate)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from django.urls import path, include

from .views import CustomTokenObtainPairView, ListClassesOfTeacher, ListAllAssignments
from .views import ListDetailsOfChild, ListAllNotices, ListAllAssignmentsOfClass, ListAllNoticesOfClass
from .views import PostAssignment, PostNotice
from .views import FeedbackForParent, AllFeedback, FeedbackForTeacher, PostFeedback
from .views import UpdateChildProfile, PostAttendance, PostActivity
from .views import ListAllAssignmentsForStudent, ListAllNoticesForStudent
from .views import ListAllStudentsOfClass, ListAllActivities, ListAllActivitiesOfClass, ListAllActivitiesForStudent
from .views import (FeedbackForParent, AllFeedback, FeedbackForTeacher, ListParentDetailsOfChild, ImageUploadView,
                    SyncUsersToFirebase, UpdateAssignment, UpdateActivity, UpdateNotice, AttendanceView, ReportView,
                    UserViewSet)

# FOR ADMIN

from .views import (ClassTableList, TeacherList, SubjectList, StudentList, ParentList,
                    ParentChildList, TeacherClassList, ActivityList, ActivityStudentList,
                    AssignmentList, AssignmentStudentList, AttendanceList, FeedbackStudentList,
                    NoticeList, NoticeStudentList, )

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('get_children/', ListDetailsOfChild.as_view(), name='get_child'),
    path('get_parent_details/<int:studentid>', ListParentDetailsOfChild.as_view(), name='get_parent_deatil'),
    path('classes/<int:teacher_id>/', ListClassesOfTeacher.as_view(), name='get_classes_of_teacher'),

    path('students/', StudentListCreate.as_view(), name='get_students'),
    path('students/<int:class_id>/', StudentListCreate.as_view(), name='get_students_of_class'),

    path('get_all_assignments/', ListAllAssignments.as_view(), name='get_all_assignment'),
    path('get_all_assignments_of_class/<int:classid>/', ListAllAssignmentsOfClass.as_view(),
         name='get_all_class_assignments'),
    path('get_all_assignments_for_student/<int:studentid>/', ListAllAssignmentsForStudent.as_view(),
         name='get_all_student_assignments'),
    path('get_all_notices/', ListAllNotices.as_view(), name='get_all_notices'),
    path('get_all_notices_of_class/<int:classid>', ListAllNoticesOfClass.as_view(), name='get_all_class_notices'),
    path('get_all_notices_for_student/<int:studentid>', ListAllNoticesForStudent.as_view(),
         name='get_all_student_notices'),

    path('get_all_activities/', ListAllActivities.as_view(), name='get_all_activities'),
    path('get_all_activities_of_class/<int:classid>', ListAllActivitiesOfClass.as_view(), name='get_all_activities'),
    path('get_all_activities_for_student/<int:studentid>', ListAllActivitiesForStudent.as_view(),
         name='get_all_student_activities'),

    path('post_assignment/', PostAssignment.as_view(), name='post_assignment'),
    path('post_notice/', PostNotice.as_view(), name='post_notice'),
    path("post_feedback/", PostFeedback.as_view(), name='post_feedback'),
    path("post_attendance/", PostAttendance.as_view(), name='post_attendance'),
    path("post_activity/", PostActivity.as_view(), name='post_actvity'),

    path('attendance/<int:student_id>/', AttendanceView.as_view(),name='attendance_by_student_id'),

    path('report_card/<int:student_id>/', ReportView.as_view(), name='get_attednance_by_student'),
    path('report_card/', ReportView.as_view(), name='post_report_card'),

    path('get_feedback_for_parent/<int:studentid>', FeedbackForParent.as_view(), name='get_feedback_for_parent'),
    path('get_all_feedback/', AllFeedback.as_view(), name='get_all_feedback'),
    path('get_feedback_for_teacher/<int:teacherid>', FeedbackForTeacher.as_view(), name="get_feedback_for_teacher"),

    path('update_child_profile/<int:studentid>/', UpdateChildProfile.as_view(), name='update_child_profile'),
    path('assignment/<int:id>/', UpdateAssignment.as_view(), name="update_assignment"),
    path('activity/<int:id>/', UpdateActivity.as_view(), name="update_activity"),
    path('notice/<int:id>/', UpdateNotice.as_view(), name="update_notice"),

    path('admin/class_table/', ClassTableList.as_view(), name='class_table'),
    path('admin/class_table/<int:pk>', ClassTableList.as_view(), name='class_table'),

    path('admin/student/', StudentList.as_view(), name='student'),
    path('admin/student/<int:pk>', StudentList.as_view(), name='student'),

    path('admin/parent/', ParentList.as_view(), name='parent'),
    path('admin/parent/<int:pk>', ParentList.as_view(), name='parent'),

    path('admin/parent_child/', ParentChildList.as_view(), name='parent_child'),
    path('admin/parent_child/<int:pk>', ParentChildList.as_view(), name='parent_child'),

    path('admin/teacher/', TeacherList.as_view(), name='teacher'),
    path('admin/teacher/<int:pk>', TeacherList.as_view(), name='teacher'),

    path('admin/subject/', SubjectList.as_view(), name='subject'),
    path('admin/subject/<int:pk>', SubjectList.as_view(), name='subject'),

    path('admin/teacher_class/', TeacherClassList.as_view(), name='teacher_class'),
    path('admin/teacher_class/<int:pk>', TeacherClassList.as_view(), name='teacher_class'),

    path('admin/assignment/', AssignmentList.as_view(), name='assignment'),
    path('admin/assignment/<int:pk>', AssignmentList.as_view(), name='assignment'),

    path('admin/assignment_student/', AssignmentStudentList.as_view(), name='assignment_student'),
    path('admin/assignment_student/<int:pk>', AssignmentStudentList.as_view(), name='assignment_student'),

    path('admin/notice/', NoticeList.as_view(), name='notice'),
    path('admin/notice/<int:pk>', NoticeList.as_view(), name='notice'),

    path('admin/notice_student/', NoticeStudentList.as_view(), name='notice_student'),
    path('admin/notice_student/<int:pk>', NoticeStudentList.as_view(), name='notice_student'),

    path('admin/activity/', ActivityList.as_view(), name='activity'),
    path('admin/activity/<int:pk>', ActivityList.as_view(), name='activity'),

    path('admin/activity_student/', ActivityStudentList.as_view(), name='activity_student'),
    path('admin/activity_student/<int:pk>', ActivityStudentList.as_view(), name='activity_student'),

    path('admin/feedback_student/', FeedbackStudentList.as_view(), name='feedback_student'),
    path('admin/feedback_student/<int:pk>', FeedbackStudentList.as_view(), name='feedback_student'),

    path('admin/attendance/', AttendanceList.as_view(), name='attendance'),
    path('admin/attendance/<int:pk>', AttendanceList.as_view(), name='attendance'),
    path('admin/sync/users/', SyncUsersToFirebase.as_view(), name='sync_users'),

    path('admin/user/', UserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('admin/user/<int:pk>/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
        'patch': 'partial_update',
    })),

    path('image/<str:data_type>/<int:id>/', ImageUploadView.as_view(), name='post_image')

]
