from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.register, name='register'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('jobs/', views.job_list, name='job_list'),
    path('post-job/', views.post_job, name='post_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('recommend/', views.recommend_jobs, name='recommend_jobs'),

]
