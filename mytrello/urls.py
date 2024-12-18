"""
URL configuration for mytrello project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('create_task/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('taks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('perfil_usuario/<int:user_id>/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil_usuario/<int:user_id>/perfil_detalle/', views.perfil_detalle, name='perfil_detalle'),

    path('espacios/', views.espacios, name='espacios'),
    path('crear_espacio/', views.crear_espacio, name='crear_espacio'),
    path('espacio/<int:espacio_id>/activar_espacio/', views.activar_espacio, name='activar_espacio'),
    path('espacio/<int:espacio_id>/inactivar_espacio/', views.inactivar_espacio, name='inactivar_espacio'),
    path('espacio/<int:espacio_id>/espacio_detalle/', views.espacio_detalle, name='espacio_detalle'),

    path('espacio/<int:espacio_id>/tableros/', views.tableros, name='tableros'), 
    path('espacio/<int:espacio_id>/crear_tablero/', views.crear_tablero, name='crear_tablero'),
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/tablero_detalle/', views.tablero_detalle, name='tablero_detalle'),
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/eliminar_tablero/', views.eliminar_tablero, name='eliminar_tablero'),

    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/listas/', views.listas, name='listas'),
    path('update_list_order/<int:tablero_id>/<int:list_id>/<int:new_index>/', views.update_list_order, name='update_list_order'),

    
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/crear_lista/', views.crear_lista, name='crear_lista'),
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/lista/<int:lista_id>/lista_detalle/', views.lista_detalle, name='lista_detalle'),
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/lista/<int:lista_id>/eliminar_lista/', views.eliminar_lista, name='eliminar_lista'),
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/lista/<int:lista_id>/lista_mover_derecha/', views.lista_mover_derecha, name='lista_mover_derecha'),
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/lista/<int:lista_id>/lista_mover_izquierda/', views.lista_mover_izquierda, name='lista_mover_izquierda'),
    
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/lista/crear_tarjeta/', views.crear_tarjeta, name='crear_tarjeta'), 
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/lista/<int:lista_id>/tarjeta/<int:tarjeta_id>/tarjeta_detalle/', views.tarjeta_detalle, name='tarjeta_detalle'), 
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/lista/<int:lista_id>/tarjeta/<int:tarjeta_id>/eliminar_tarjeta/', views.eliminar_tarjeta, name='eliminar_tarjeta'), 

    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/lista/<int:lista_id>/tarjeta/<int:tarjeta_id>/crear_tarea/', views.crear_tarea, name='crear_tarea'), 
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/lista/<int:lista_id>/tarjeta/<int:tarjeta_id>/tarea/<int:tarea_id>/tarea_detalle/', views.tarea_detalle, name='tarea_detalle'), 
    path('espacio/<int:espacio_id>/tablero/<int:tablero_id>/lista/<int:lista_id>/tarjeta/<int:tarjeta_id>/tarea/<int:tarea_id>/eliminar_tarea/', views.eliminar_tarea, name='eliminar_tarea'),

    path('espacio/tablero/<int:tablero_id>/lista/dashboard/', views.dashboard, name='dashboard'),  
]
# + staticfiles_urlpatterns()