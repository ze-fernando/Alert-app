from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('task', views.create_task, name='task'),
    path('tasks/<int:id>', views.tasks, name='tasks'),
    path('del/<int:id>', views.del_task, name='del'),
    path('edit/<int:id>', views.put_task, name='put')
]