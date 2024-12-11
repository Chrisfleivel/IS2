from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.shortcuts import render
from django.db.models import Count
from datetime import date

from .models import Task, EspacioDeTrabajo, Tablero, Lista, Tarjeta, Tarea, Perfil

from .forms import TaskForm, EspacioDeTrabajoForm, TableroForm, ListaForm, TarjetaForm, TareaForm, FiltroTarjetasForm, FiltroTarjetasEtiquetaForm, PerfilForm
from .decorador import miembro_requerido
# from django.urls import reverse



def signup(request):
    '''Valida el Registro del usuario
        - usuario:
        - contraseña1
        - contraseña2'''
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)

                return redirect('perfil_usuario', user_id=user.id)
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

def home(request):
    '''Paguina de inicio'''
    return render(request, 'home.html')

def signin(request):
    '''Valida el Inicio de Sesion del Usuario
        - usuario
        - contraseña'''
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('perfil_usuario', user_id=user.id)

@login_required
def signout(request):
    '''Cierra la secion del Usuario'''
    logout(request)
    return redirect('home')



@login_required 
def perfil_usuario(request, user_id):
    # Verificar si el usuario actual es el que se está consultando

    try:
        perfil = Perfil.objects.get(user=request.user)
    except Perfil.DoesNotExist:
        # Crear el perfil si no existe
        perfil = Perfil.objects.create(user=request.user, nombre_usuario=request.user.username)

    context = {'perfil': perfil}
    return render(request, 'perfil.html', context)
 
@login_required    
def perfil_usuario2(request, user_id):
    user = get_object_or_404(User, pk=request.user.id)
    try:
        perfil = get_object_or_404(Perfil, user=user)
    except IntegrityError:
        nombre= user.username
        perfil1= Perfil(user=user, nombre_usuario=nombre)
        perfil.save()
        perfil = get_object_or_404(Perfil, user=user)
    
    context = {'perfil': perfil}
    return render(request, 'perfil.html', context)



@login_required
def perfil_detalle(request, user_id):
    '''Permite a los usuario la gestion de los espacios de trabajos'''
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'GET':
       
        perfil = get_object_or_404(Perfil, user=user)
        form = PerfilForm(instance=perfil)
        return render(request, 'perfil_detalle.html', {'perfil': perfil, 'form': form})
    else:
        try:
            perfil = get_object_or_404(Perfil, user=user)
            form = PerfilForm(request.POST, instance=perfil)
            form.save()
            return redirect('perfil_usuario', user_id=user_id)     
        except ValueError:
            return render(request, 'espacios_detalle.html', {'perfil': perfil, 'form': form, 'error': 'Error al actualizar Espacio.'})
  

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        # Lógica para procesar el formulario y actualizar el perfil
        # ...
        return redirect('perfil_usuario')  # Redirige al perfil del usuario después de guardar los cambios
    else:
        # Mostrar el formulario de edición
        # ...
        pass
     



@login_required
def espacios(request):
    '''Brinda al usuario los espacios de trabajo en que es parte de los miembros '''
    espacios = EspacioDeTrabajo.objects.filter(miembros = request.user)
    user = request.user
    return render(request, 'espacios.html', {"espacios": espacios, 'user': user})

@login_required
def crear_espacio(request):
    '''Permite a los usuarios Crear Espacios de Trabajos '''
    if request.method == "GET":
        return render(request, 'crear_espacio.html', {"form": EspacioDeTrabajoForm})
    else:
        try:
            form = EspacioDeTrabajoForm(request.POST)
            new_espacio = form.save(commit=False)
            new_espacio.creador = request.user
            new_espacio.save()
            # Agregar los miembros seleccionados
            new_espacio.miembros.add(*form.cleaned_data['miembros'])
            print(new_espacio.miembros.all())
            return redirect('espacios')
        except ValueError:
            return render(request, 'crear_espacio.html', {"form": EspacioDeTrabajoForm, "error": "Error al crear Espacio de Trabajo."})

@login_required
def espacio_detalle(request, espacio_id):
    '''Permite a los usuario la gestion de los espacios de trabajos'''
    if request.method == 'GET':
        espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
        form = EspacioDeTrabajoForm(instance=espacio)
        return render(request, 'espacios_detalle.html', {'espacio': espacio, 'form': form})
    else:
        try:
            espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
            form = EspacioDeTrabajoForm(request.POST, instance=espacio)
            form.save()
            return redirect('espacios')
        except ValueError:
            return render(request, 'espacios_detalle.html', {'espacio': espacio, 'form': form, 'error': 'Error al actualizar Espacio.'})
      
@login_required
def inactivar_espacio(request, espacio_id):
    espacio = get_object_or_404(EspacioDeTrabajo, id=espacio_id)
    if espacio.es_creador(request.user):
        espacio.activo = False
        espacio.save()
        return redirect('espacios')  # Redirige a la lista de espacios
    else:
        # Mostrar un mensaje de error o redirigir a otra página
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para inactivar este espacio.'})
    
@login_required
def activar_espacio(request, espacio_id):
    espacio = get_object_or_404(EspacioDeTrabajo, id=espacio_id)
    if espacio.es_creador(request.user):
        espacio.activo = True
        espacio.save()
        return redirect('espacios')  # Redirige a la lista de espacios
    else:
        # Mostrar un mensaje de error o redirigir a otra página
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para inactivar este espacio.'})




@login_required
def tableros(request, espacio_id):
    '''Inicia los tableros que posee el espacio de trabajo. 
    Solo pueden ingresar los miembros del espacio de trabajo'''
    espacio = get_object_or_404(EspacioDeTrabajo, id=espacio_id)
    tableros = Tablero.objects.filter(espacio_trabajo = espacio)
    return render(request, 'tableros.html', {"tableros": tableros, "espacio": espacio})

@login_required
def crear_tablero(request, espacio_id):
    '''Permite a los usuarios Crear Tableros en el Espacio de Trabajo '''
    espacio = get_object_or_404(EspacioDeTrabajo, id=espacio_id)
    
    if request.method == "POST":
        try:
            form = TableroForm(request.POST)
            new_espacio = form.save(commit=False)
            new_espacio.espacio_trabajo = espacio
            new_espacio.save()
            return redirect('tableros', espacio_id=espacio_id)
        except ValueError:
            return render(request, 'crear_tablero.html', {"form": TableroForm, "error": "Error al crear Tablero", "espacio": espacio})
    else: 
        return render(request, 'crear_tablero.html', {"form": TableroForm, "espacio": espacio})
    
@login_required
def tablero_detalle(request, espacio_id, tablero_id):
    '''Permite a los usuario la gestion de los espacios de trabajos'''
    if request.method == 'GET':
        espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
        tablero = get_object_or_404(Tablero, pk=tablero_id)
        form = TableroForm(instance=tablero)
        return render(request, 'tablero_detalle.html', {'espacio': espacio, 'form': form, 'tablero': tablero})
    else:
        try:
            espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
            tablero = get_object_or_404(Tablero, pk=tablero_id)
            form = TableroForm(request.POST, instance=tablero)
            form.save()
            return redirect('tableros', espacio_id=espacio_id)
        except ValueError:
            return render(request, 'espacios_detalle.html', {'espacio': espacio, 'form': form, 'error': 'Error al actualizar Espacio.', 'tablero': tablero})

@login_required
def eliminar_tablero(request, espacio_id, tablero_id):
    tablero = get_object_or_404(Tablero, pk=tablero_id)
    if request.method == 'POST':
        tablero.delete()
        return redirect('tableros', espacio_id=espacio_id)
    else:
        # Mostrar un mensaje de error o redirigir a otra página
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para inactivar este espacio.'})
    






@login_required
def listas(request, espacio_id, tablero_id):
    espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
    tablero = get_object_or_404(Tablero, pk=tablero_id)
    tarjetas_filtro = None
    actualizar_estado_tareas()
    if request.method == 'POST':
        # Crear instancias de los formularios con prefijos para los nombres
        form1 = FiltroTarjetasForm(request.POST, usuarios=espacio.miembros.all())
        form2 = FiltroTarjetasEtiquetaForm(request.POST)

        if form2.is_valid():
            etiqueta = form2.cleaned_data['etiqueta']
            tarjetas_filtro2 = Tarjeta.objects.filter(etiqueta=etiqueta)
        if form1.is_valid():
            usuario_seleccionado = form1.cleaned_data['usuario_asignado']
            tarjetas_filtro1 = Tarjeta.objects.filter(usuario_asignado=usuario_seleccionado)
        if tarjetas_filtro2:
            tarjetas_filtro = tarjetas_filtro2
        if tarjetas_filtro1:
            tarjetas_filtro = tarjetas_filtro1      
    else:
        form1 = FiltroTarjetasForm(usuarios=espacio.miembros.all())
        form2 = FiltroTarjetasEtiquetaForm()
        tarjetas_filtro = Tarjeta.objects.all()  # Obtener todas las tarjetas por defecto
    # Obtener las listas asociadas al tablero
    listas = tablero.listas.all()  
    context = {'espacio': espacio, 'tablero': tablero, 'listas': listas, 'tarjetas_filtro':tarjetas_filtro, 'form_u':form1, 'form_e':form2 }
    return render(request, 'listas.html', context)




@login_required
def crear_lista(request, espacio_id, tablero_id):
    espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
    tablero = get_object_or_404(Tablero, id=tablero_id)

    if request.method == 'POST':
        form = ListaForm(request.POST)
        if form.is_valid():
            lista = form.save(commit=False)
            lista.tablero = tablero
            lista.save()
            tablero.agregar_lista(lista) 
            return redirect('listas', tablero_id=tablero_id, espacio_id=espacio_id)
    else:
        return render(request, 'crear_lista.html', {'form': ListaForm, 'tablero': tablero, 'espacio': espacio})

@login_required
def lista_detalle(request, espacio_id, tablero_id, lista_id):
    '''Permite a los usuario la gestion de los espacios de trabajos'''
    if request.method == 'GET':
        espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
        tablero = get_object_or_404(Tablero, pk=tablero_id)
        lista = get_object_or_404(Lista, pk=lista_id)
        form = ListaForm(instance=lista)
        return render(request, 'lista_detalle.html', {'espacio': espacio, 'form': form, 'tablero': tablero, 'lista': lista})
    else:
        try:
            espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
            tablero = get_object_or_404(Tablero, pk=tablero_id)
            lista = get_object_or_404(Lista, pk=lista_id)
            form = ListaForm(request.POST, instance=lista)
            form.save()
            return redirect('listas', espacio_id=espacio_id, tablero_id=tablero.id)
        except ValueError:
            return render(request, 'lista_detalle.html', {'espacio': espacio, 'form': form, 'error': 'Error al actualizar Espacio.', 'tablero': tablero, 'lista': lista})

@login_required
def eliminar_lista(request, espacio_id, tablero_id, lista_id):
    espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
    tablero = get_object_or_404(Tablero, pk=tablero_id)
    lista = get_object_or_404(Lista, pk=lista_id)
    print(espacio)
    if request.method == 'POST':
        tablero.eliminar_lista(lista)
        tablero.save()
        lista.delete()
        return redirect('listas', espacio_id=espacio_id, tablero_id=tablero.id)
        
@login_required
def lista_mover_derecha(request, espacio_id, tablero_id, lista_id):
    espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
    tablero = get_object_or_404(Tablero, pk=tablero_id)
    lista1 = get_object_or_404(Lista, pk=lista_id)
    if request.method == 'GET':
        ultima_lista = tablero.listas.last()
        if ultima_lista.orden > lista1.orden:
            for r_lista in tablero.listas.all():
                if r_lista.orden == (lista1.orden + 1):
                    lista2 = r_lista
            tablero.cambiar_orden(lista1, lista2)
    return redirect('listas', espacio_id=espacio_id, tablero_id=tablero_id)

@login_required
def lista_mover_izquierda(request, espacio_id, tablero_id, lista_id):
    espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
    tablero = get_object_or_404(Tablero, pk=tablero_id)
    lista1 = get_object_or_404(Lista, pk=lista_id)
    if request.method == 'GET':
        if lista1.orden != 0 :
            for r_lista in tablero.listas.all():
                if r_lista.orden == (lista1.orden - 1):
                    lista2 = r_lista
            tablero.cambiar_orden(lista2, lista1)
    return redirect('listas', espacio_id=espacio_id, tablero_id=tablero_id)
    





@login_required
def update_list_order(request, tablero_id, list_id, new_index):
    print("entro actualizar lis")
    tablero = get_object_or_404(Tablero, pk=tablero_id)
    print(tablero)
    if request.method == 'POST':
        print("entro pos")
        
        try:
            for lista_t in tablero.listas.all():
                if lista_t.orden == list_id:
                    lista = lista_t
            if lista.orden == new_index:
                return JsonResponse({'message': 'Lista actualizada correctamente', 'success': True})
            elif lista.orden > new_index:
                if lista.orden != 0: 
                    while lista.orden > new_index:
                        for r_lista in tablero.listas.all():
                            if r_lista.orden == (lista.orden - 1):
                                lista2 = r_lista
                        tablero.cambiar_orden(lista2, lista)
            else:
                ultima_lista = tablero.listas.last()
                if ultima_lista.orden > lista.orden:
                    while lista.orden < new_index:
                        for r_lista in tablero.listas.all():
                            if r_lista.orden == (lista.orden + 1):
                                lista2 = r_lista
                        tablero.cambiar_orden(lista, lista2)
            return JsonResponse({'message': 'Lista actualizada correctamente'})
        except Lista.DoesNotExist:
            return JsonResponse({'error': 'Lista no encontrada'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



def crear_tarjeta(request, espacio_id, tablero_id):
    espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
    tablero = get_object_or_404(Tablero, id=tablero_id)

    if request.method == 'POST':
        form = TarjetaForm(request.POST) 
        if form.is_valid():
            tarjeta = Tarjeta
            tarjeta = form.save(commit=False)
            # obtener estado y usuario
            estado = form.cleaned_data['estado']
            usuario_asignado = form.cleaned_data['usuario_asignado']
            # Asignar estado y usuario directamente
            tarjeta.estado = estado
            tarjeta.usuario_asignado = usuario_asignado
            tarjeta.save()
            estado.agregar_tarjeta(tarjeta)        
            return redirect('listas', tablero_id=tablero_id, espacio_id=espacio_id)
    else:
        form = TarjetaForm()
        form.introducir_estados(tablero.listas.all())
        print(espacio.miembros.all())
        form.introducir_usuarios(espacio.miembros.all())
        # print(form.errors)  # Imprime los errores del formulario en la consola
    context = {'form': form, 'tablero': tablero, 'espacio': espacio}
    return render(request, 'crear_tarjeta.html', context)

@login_required
def eliminar_tarjeta(request, espacio_id, tablero_id, lista_id, tarjeta_id):
    espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
    tablero = get_object_or_404(Tablero, pk=tablero_id)
    lista = get_object_or_404(Lista, pk=lista_id)
    tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
    print(espacio)
    if request.method == 'POST':
        lista.eliminar_tarjeta(tarjeta)
        tarjeta.delete()
        return redirect('listas', espacio_id=espacio_id, tablero_id=tablero.id)

@login_required
def tarjeta_detalle(request, espacio_id, tablero_id, lista_id, tarjeta_id):
    '''Permite a los usuario la gestion de los espacios de trabajos'''
    if request.method == 'GET':
        espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
        tablero = get_object_or_404(Tablero, pk=tablero_id)
        lista = get_object_or_404(Lista, pk=lista_id)
        tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
        form = TarjetaForm(instance=tarjeta)
        form.introducir_usuarios(espacio.miembros.all())
        form.introducir_estados(tablero.listas.all())
        return render(request, 'tarjeta_detalle.html', {'espacio': espacio, 'form': form, 'tablero': tablero, 'lista': lista, 'tarjeta':tarjeta})
    else:
        try:
            espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
            tablero = get_object_or_404(Tablero, pk=tablero_id)
            lista = get_object_or_404(Lista, pk=lista_id)
            tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
            form = TarjetaForm(request.POST, instance=tarjeta)
            form.save()
            if lista != tarjeta.estado:
                print("cambio de lista")
                lista.eliminar_tarjeta(tarjeta) 
                tarjeta.estado.agregar_tarjeta(tarjeta)
            return redirect('listas', espacio_id=espacio_id, tablero_id=tablero.id)
        except ValueError:
            return render(request, 'tarjeta_detalle.html', {'espacio': espacio, 'form': form, 'error': 'Error al actualizar Espacio.', 'tablero': tablero, 'lista': lista, 'tarjeta':tarjeta})

      

            

def crear_tarea(request, espacio_id, tablero_id, lista_id, tarjeta_id):
    espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
    tablero = get_object_or_404(Tablero, id=tablero_id)
    lista = get_object_or_404(Lista, pk=lista_id)
    tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
    if request.method == 'POST':
        form = TareaForm(request.POST) 
        if form.is_valid():
            tarea = Tarea
            tarea = form.save(commit=False)
            # obtener usuario
            usuario_asignado = form.cleaned_data['usuario_asignado']
            # Asignar  usuario directamente
            tarea.usuario_asignado = usuario_asignado
            tarea.save()
            tarjeta.agregar_tarea(tarea)        
            return redirect('listas', tablero_id=tablero_id, espacio_id=espacio_id)
    else:
        form = TareaForm()
        form.introducir_usuarios(espacio.miembros.all())
    context = {'form': form, 'tablero': tablero, 'espacio': espacio, 'lista':lista, 'tarjeta':tarjeta}
    return render(request, 'crear_tarea.html', context)

@login_required
def eliminar_tarea(request, espacio_id, tablero_id, lista_id, tarjeta_id, tarea_id):
    espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
    tablero = get_object_or_404(Tablero, pk=tablero_id)
    lista = get_object_or_404(Lista, pk=lista_id)
    tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    print(espacio)
    if request.method == 'POST':
        tarjeta.eliminar_tarea(tarea)
        tarea.delete()
        return redirect('listas', espacio_id=espacio_id, tablero_id=tablero.id)

@login_required
def tarea_detalle(request, espacio_id, tablero_id, lista_id, tarjeta_id, tarea_id):
    '''Permite a los usuario la gestion de los espacios de trabajos'''
    if request.method == 'GET':
        espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
        tablero = get_object_or_404(Tablero, pk=tablero_id)
        lista = get_object_or_404(Lista, pk=lista_id)
        tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
        tarea = get_object_or_404(Tarea, pk=tarea_id)
        form = TareaForm(instance=tarea)
        form.introducir_usuarios(espacio.miembros.all())
        return render(request, 'tarea_detalle.html', {'espacio': espacio, 'form': form, 'tablero': tablero, 'lista': lista, 'tarjeta':tarjeta, 'tarea':tarea})
    else:
        try:
            espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
            tablero = get_object_or_404(Tablero, pk=tablero_id)
            lista = get_object_or_404(Lista, pk=lista_id)
            tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
            tarea = get_object_or_404(Tarea, pk=tarea_id)
            form = TareaForm(request.POST, instance=tarea)
            form.save()
            return redirect('listas', espacio_id=espacio_id, tablero_id=tablero.id)
        except ValueError:
            return render(request, 'tarea_detalle.html', {'espacio': espacio, 'form': form, 'error': 'Error al actualizar Espacio.', 'tablero': tablero, 'lista': lista, 'tarjeta':tarjeta, 'tarea':tarea})

def actualizar_estado_tareas():
    tareas = Tarea.objects.all()
    for tarea in tareas:
        print(tarea.fecha_vencimiento)
        print(timezone.now())
        if tarea.fecha_vencimiento <= timezone.now():
            print("entro")
            tarea.atrasada = True
            tarea.save()




@login_required
def dashboard2(request, tablero_id):
    tablero = get_object_or_404(Tablero, pk=tablero_id)
    listas = tablero.listas.all()
    tarjetas = []
    tareas = []
    for lista in listas:
        for tarjeta in lista.tarjetas.all():
            tarjetas.append(tarjeta)  
        for tarjeta in lista.tarjetas.all():
            for tarea in tarjeta.tareas.all():
                tareas.append(tarea)   
    # Datos para los gráficos (ejemplo con Chart.js)
    datos_estado_tarjeta = tarjetas.values('estado').annotate(total=Count('id'))
    datos_usuario_tarjeta = tarjetas.values('usuario_asignado').annotate(total=Count('id'))
    tareas_atrasadas_tarjeta = tarjetas.filter(fecha_vencimiento__lt=date.today())

    datos_estado = tareas.values('estado_cerrado').annotate(total=Count('id'))
    datos_usuario = tareas.values('usuario_asignado').annotate(total=Count('id'))
    tareas_atrasadas = tareas.filter(fecha_vencimiento__lt=date.today())

    return render(request, 'dashboard.html', {
        'tablero': tablero,
        'datos_estado': datos_estado,
        'datos_usuario': datos_usuario,
        'tareas_atrasadas': tareas_atrasadas,
        'datos_estado_tarjeta': datos_estado_tarjeta,
        'datos_usuario_tarjeta': datos_usuario_tarjeta,
        'tareas_atrasadas_tarjeta': tareas_atrasadas_tarjeta,
    })




def dashboard(request, tablero_id):
    tablero = get_object_or_404(Tablero, pk=tablero_id)

    # Obtener todas las tarjetas relacionadas con el tablero
    tarjetas = tablero.listas.all().prefetch_related('tarjetas').values_list('tarjetas', flat=True)
    print(tarjetas)

    # Obtener todas las tareas de las tarjetas
    # Obtener todas las tareas relacionadas con el tablero
    tareas = tablero.listas.all().prefetch_related('tarjetas__tareas').values_list('tarjetas__tareas', flat=True)
    print(tareas)
    # Crear un QuerySet de Tarea a partir de los IDs obtenidos
    tareas_queryset = Tarea.objects.filter(pk__in=tareas)

    # Datos para los gráficos
    datos_usuario_tarea = tareas_queryset.values('usuario_asignado').annotate(total=Count('usuario_asignado_id'))
    tareas_atrasadas = tareas_queryset.filter(fecha_vencimiento__lt=date.today()).count()

    # Datos para el gráfico de estados de tarjeta
    datos_estado_tarjeta = tarjetas.values('tarjeta_estado').annotate(total=Count('nombre'))

    return render(request, 'dashboard.html', {
        'tablero': tablero,
        'datos_usuario_tarea': datos_usuario_tarea,
        'tareas_atrasadas': tareas_atrasadas,
        'datos_estado_tarjeta': datos_estado_tarjeta
    })























@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
   