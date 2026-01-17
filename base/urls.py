from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    # Home and Team URLs
    path('', views.home, name="home"),
    path('team', views.team, name="team"),

    # Time Management URL
    path('time-management', views.timeManagement, name="time-management"),

    # Calendar URLs
    path('calendar', views.calendar, name="calendar"),
    path('all-events/', views.all_events, name="all-events"),
    path('add-event/', views.add_event, name="add-event"),
    path('update/', views.update, name="update"),
    path('remove/', views.update, name="remove"),

    # Task Management URLs
    path('task-management', views.todoList, name="tasks"),
    path('task-management/complete/<int:pk>', views.complete_task, name="complete-task"),
    path('task-management/task/<int:pk>/task-delete', views.taskDelete, name='task-delete'),

    # Forums URLs
    path('forums', views.forums, name="forums"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>', views.userPofile, name="user-profile"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]
