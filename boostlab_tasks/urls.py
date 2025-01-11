
from django.urls import include, path
from . import views
urlpatterns = [
    path('my-tasks/',views.my_tasks_view,name="my-tasks"), 
    path('task/create/',views.task_create_view,name="create-task"),
    path('task/<int:pk>/',views.task_detail_view,name="task-detail"), 
    path('task/delete/<int:pk>/',views.task_delete_view,name="delete-task"),
    path('task/edit/<int:pk>/',views.task_edit_view,name="edit-task"),
    
    path('activity/<int:pk>/',views.activity_create_view,name="create-activity"),
    path('activity/delete/<int:pk>/',views.activity_delete_view,name="delete-activity"),
    
    
    path('file/<int:pk>/',views.file_create_view,name="create-file"),
    path('file/delete/<int:pk>/',views.file_delete_view,name="delete-file"),     
 ]
