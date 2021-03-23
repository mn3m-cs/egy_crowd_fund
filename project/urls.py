from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create_project/', views.ProjectCreateView.as_view(), name='create_project'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_details'),
    path('my_projects/',views.my_projects,name='my_projects'),
    path('donate/<project>/',views.donate,name='donate'),
    path('my_donations/',views.my_donations,name='my_donations'),
    path('rate/<project>/',views.rate,name='rate'),
    path('comment/<project>/',views.comment,name='comment'),
    path('report_project/<project>/',views.report_project,name='report_project'),
    path('report_comment/<c_pk>/<project>/',views.report_comment,name='report_comment')

]
