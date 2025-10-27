from django.urls import path
from core import views
from core.views import JobRoleAutocomplete

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload_resume/', views.upload_resume, name='upload_resume'),
    path('mock-interview/', views.mock_interview, name='mock_interview'),
    path('reports/', views.reports, name='reports'),
    path('generate-questions/', views.generate_questions, name='generate_questions'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('analyze_answer/', views.analyze_answer, name='analyze_answer'),
    path('report/<int:id>/', views.view_report, name='view_report'),
    path('job-role-autocomplete/', JobRoleAutocomplete.as_view(), name='job-role-autocomplete'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('api/transcribe-chunk/', views.transcribe_chunk, name='transcribe_chunk'),
]
