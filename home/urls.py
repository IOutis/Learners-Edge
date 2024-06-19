from django.contrib import admin
from django.urls import path, include
from home import views
from register import views as v
from django.contrib.auth import views as auth_views
# from notifications_app.consumers import NotificationConsumer
import notifications.urls
from notes import views as notes_views
import django_ckeditor_5.views as ck_views

urlpatterns = [
    path('', views.index, name="Home"), # Root URL
    path('home/', views.index, name="Home"), # Root URL
    path('about/', views.about, name="About"),
    path('services/', views.services, name="Services"),
    path('dashboard/', views.dashboard, name="Dashboard"),
    path('contact/', views.contact, name="Contact"),
    path('pomodoro/', views.pomodoro, name="Pomodoro"),
    path('register/', v.register, name="register"),
    path('timetable/', views.timetable, name="TimeTable"),
    path("save/", views.save, name="SaveTask"),
    path("notes/", views.notes, name="Notes"),
    path("get/", views.get_in_progress, name="GetTimetable"),
    path("get_notdone/", views.getnotdone, name="GetTimetable"),
    path("get_done/", views.getcompleted, name="GetTimetable"),
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
    
    
    path('test/', views.test, name="home"),
    path('testing/<int:notification_id>/', views.testing, name="home"),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path("", include('django.contrib.auth.urls')),
    path('user_logout/', v.user_logout, name='logout'),
    # path('ws/notifications/', NotificationConsumer.as_asgi()),
    # path('ws/user/<str:user_id>/', NotificationConsumer.as_asgi()),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),
     path('mark_notification_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
     
     
     path('chatbot/', views.react_app, name='react_app'),
     
    
     path("ckeditor5/", include('django_ckeditor_5.urls')),
     path('ckeditor5/image_upload/', ck_views.upload_file, name="ck_editor_5_upload_file"),
     path('new_notes/', views.create_note, name='create_note'),
     path('note_detail/<int:note_id>/', views.note_detail, name='note_detail'),
     path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)