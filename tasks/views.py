from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Task, EspacioDeTrabajo, Tablero, Lista, Tarjeta

from .forms import TaskForm, EspacioDeTrabajoForm, TableroForm, ListaForm, TarjetaForm
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
    user = get_object_or_404(User, pk=user_id)
    context = {'usuario': user}
    return render(request, 'perfil.html', context)

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
    # Obtener las listas asociadas al tablero
    listas = tablero.listas.all()  
    return render(request, 'listas.html', {'espacio': espacio, 'tablero': tablero, 'listas': listas })

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
    print("l1:", lista1.orden)
    if request.method == 'GET':
        ultima_lista = tablero.listas.last()
        print("ultimo", ultima_lista.orden)
        if ultima_lista.orden > lista1.orden:
            for r_lista in tablero.listas.all():
                if r_lista.orden == (lista1.orden + 1):
                    lista2 = r_lista
            print("l2:", lista2.orden)
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
    



def crear_tarjeta(request, espacio_id, tablero_id, lista_id):
    espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
    tablero = get_object_or_404(Tablero, id=tablero_id)
    lista = get_object_or_404(Lista, id=lista_id)

    if request.method == 'POST':
        form = TarjetaForm(request.POST) 
        if form.is_valid():
            tarjeta = form.save(commit=False)
            tarjeta.lista = lista 
            tarjeta.save()
            lista.agregar_tarjeta(tarjeta) 
            return redirect('listas', tablero_id=tablero_id, espacio_id=espacio_id)
    else:
        form = TarjetaForm()
        # print(form.errors)  # Imprime los errores del formulario en la consola

    # Pasa los miembros al contexto 
    context = {'form': form, 'tablero': tablero, 'espacio': espacio, 'lista':lista}
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
        return render(request, 'lista_detalle.html', {'espacio': espacio, 'form': form, 'tablero': tablero, 'lista': lista, 'tarjeta':tarjeta})
    else:
        try:
            espacio = get_object_or_404(EspacioDeTrabajo, pk=espacio_id, miembros=request.user)
            tablero = get_object_or_404(Tablero, pk=tablero_id)
            lista = get_object_or_404(Lista, pk=lista_id)
            tarjeta = get_object_or_404(Tarjeta, pk=tarjeta_id)
            form = ListaForm(request.POST, instance=tarjeta)
            form.save()
            return redirect('listas', espacio_id=espacio_id, tablero_id=tablero.id)
        except ValueError:
            return render(request, 'lista_detalle.html', {'espacio': espacio, 'form': form, 'error': 'Error al actualizar Espacio.', 'tablero': tablero, 'lista': lista, 'tarjeta':tarjeta})

      

            





















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
   