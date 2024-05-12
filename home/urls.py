from django.contrib import admin
from django.urls import path, include
from home import views
from register import views as v
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name="Home"), # Root URL
    path('home/', views.index, name="Home"), # Root URL
    path('/', views.index, name="Home"), # Root URL
    path('about/', views.about, name="About"),
    path('services/', views.services, name="Services"),
    path('dashboard/', views.dash, name="Dashboard"),
    path('contact/', views.contact, name="Contact"),
    path('pomodoro/', views.pomodoro, name="Pomodoro"),
    path('register/', v.register, name="register"),
    path('timetable/', views.timetable, name="TimeTable"),
    path("save/", views.save, name="SaveTask"),
    path("get/", views.gettable, name="GetTimetable"),
    path("delete_all/", views.delete_all, name="DeleteAllTasks"),
    path("delete_tasks/", views.delete_tasks, name="DeleteTasks"),
    path("return/", views.return_to_tt, name="ReturnToTimetable"),
    # path("scheduled_tasks/", views.get_scheduled_tasks, name='GetScheduledTasks'),
    path("gemini/", views.gemini, name='Chat'),
    path("chat_delete/", views.chat_delete, name='Chat'),
    path("chat/", views.chat, name='Chatting'),
    # path("tasklist/", views.Task_template, name='Tasking'),
    # path("task/", views.getList, name='Task'),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
 
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path("", include('django.contrib.auth.urls')),
    path('user_logout/', v.user_logout, name='logout'),
]
