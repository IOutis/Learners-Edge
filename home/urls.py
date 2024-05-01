from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name="Home"), # Root URL
    path('home/', views.index, name="Home"), # Root URL
    path('about/', views.about, name="About"),
    path('services/', views.services, name="Services"),
    path('dashboard/', views.dash, name="Dashboard"),
    path('contact/', views.contact, name="Contact"),
    path('pomodoro/', views.pomodoro, name="Pomodoro"),
    path('login/', views.login, name="Login"),
    path('timetable/', views.timetable, name="TimeTable"),
    path("save/", views.save, name="SaveTask"),
    path("get/", views.gettable, name="GetTimetable"),
    path("delete_all/", views.delete_all, name="DeleteAllTasks"),
    path("delete_tasks/", views.delete_tasks, name="DeleteTasks"),
    path("return/", views.return_to_tt, name="ReturnToTimetable"),
    path("scheduled_tasks/", views.get_scheduled_tasks, name='GetScheduledTasks'),
    path("gemini/", views.gemini, name='Chat'),
    path("chat_delete/", views.chat_delete, name='Chat'),
    path("chat/", views.chat, name='Chatting'),
    path("tasklist/", views.Task_template, name='Tasking'),
    path("task/", views.getList, name='Task'),
    
]
