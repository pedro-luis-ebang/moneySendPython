# pylint: disable=no-member

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Usuario, Transaccion
from .forms import (
    UsuarioForm, TransferenciaForm, DepositoForm,
    RetiroForm, PagoServicioForm
)

def index(request):
    usuarios = Usuario.objects.all()
    return render(request, 'envios/index.html', {'usuarios': usuarios})

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado con éxito")
            return redirect('index')
    else:
        form = UsuarioForm()
    return render(request, 'envios/registrar_usuario.html', {'form': form})

def enviar_dinero(request):
    if request.method == 'POST':
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            remitente_nombre = form.cleaned_data['remitente']
            receptor_nombre = form.cleaned_data['receptor']
            monto = form.cleaned_data['monto']
            try:
                remitente = Usuario.objects.get(nombre=remitente_nombre)
                receptor = Usuario.objects.get(nombre=receptor_nombre)
            except Usuario.DoesNotExist:
                messages.error(request, "Uno de los usuarios no fue encontrado.")
                return redirect('enviar_dinero')
            if remitente.saldo >= monto and monto > 0:
                remitente.saldo -= monto
                receptor.saldo += monto
                remitente.save()
                receptor.save()
                # Registrar transacciones para ambos usuarios
                Transaccion.objects.create(
                    usuario=remitente,
                    tipo='envio',
                    monto=monto,
                    descripcion=f"Envió ${monto} a {receptor.nombre}"
                )
                Transaccion.objects.create(
                    usuario=receptor,
                    tipo='envio',
                    monto=monto,
                    descripcion=f"Recibió ${monto} de {remitente.nombre}"
                )
                messages.success(request, "Transferencia exitosa")
            else:
                messages.error(request, "Saldo insuficiente o monto inválido.")
            return redirect('index')
    else:
        form = TransferenciaForm()
    return render(request, 'envios/enviar_dinero.html', {'form': form})

def depositar_dinero(request):
    if request.method == 'POST':
        form = DepositoForm(request.POST)
        if form.is_valid():
            usuario_nombre = form.cleaned_data['usuario']
            monto = form.cleaned_data['monto']
            try:
                usuario = Usuario.objects.get(nombre=usuario_nombre)
            except Usuario.DoesNotExist:
                messages.error(request, "Usuario no encontrado.")
                return redirect('depositar_dinero')
            if monto > 0:
                usuario.saldo += monto
                usuario.save()
                Transaccion.objects.create(
                    usuario=usuario,
                    tipo='deposito',
                    monto=monto,
                    descripcion=f"Depósito de ${monto}"
                )
                messages.success(request, "Depósito exitoso")
            else:
                messages.error(request, "Monto inválido.")
            return redirect('index')
    else:
        form = DepositoForm()
    return render(request, 'envios/depositar_dinero.html', {'form': form})
def eliminar_usuario(request, usuario_id):
    print(f"🔍 Intentando eliminar usuario con ID: {usuario_id}")  # Depuración en consola
    
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        usuario.delete()
        print(f"✅ Usuario {usuario_id} eliminado correctamente")  # Confirmación en consola
        return redirect('index')  # Asegúrate de que 'index' es el nombre correcto de tu vista principal

    return redirect('index')
def retirar_dinero(request):
    if request.method == 'POST':
        form = RetiroForm(request.POST)
        if form.is_valid():
            usuario_nombre = form.cleaned_data['usuario']
            monto = form.cleaned_data['monto']
            try:
                usuario = Usuario.objects.get(nombre=usuario_nombre)
            except Usuario.DoesNotExist:
                messages.error(request, "Usuario no encontrado.")
                return redirect('retirar_dinero')
            if usuario.saldo >= monto and monto > 0:
                usuario.saldo -= monto
                usuario.save()
                Transaccion.objects.create(
                    usuario=usuario,
                    tipo='retiro',
                    monto=monto,
                    descripcion=f"Retiro de ${monto}"
                )
                messages.success(request, "Retiro exitoso")
            else:
                messages.error(request, "Saldo insuficiente o monto inválido.")
            return redirect('index')
    else:
        form = RetiroForm()
    return render(request, 'envios/retirar_dinero.html', {'form': form})

def pagar_servicio(request):
    if request.method == 'POST':
        form = PagoServicioForm(request.POST)
        if form.is_valid():
            usuario_nombre = form.cleaned_data['usuario']
            servicio = form.cleaned_data['servicio']
            monto = form.cleaned_data['monto']
            try:
                usuario = Usuario.objects.get(nombre=usuario_nombre)
            except Usuario.DoesNotExist:
                messages.error(request, "Usuario no encontrado.")
                return redirect('pagar_servicio')
            if usuario.saldo >= monto and monto > 0:
                usuario.saldo -= monto
                usuario.save()
                Transaccion.objects.create(
                    usuario=usuario,
                    tipo='pago',
                    monto=monto,
                    descripcion=f"Pago de ${monto} por {servicio}"
                )
                messages.success(request, "Pago realizado con éxito")
            else:
                messages.error(request, "Saldo insuficiente o monto inválido.")
            return redirect('index')
    else:
        form = PagoServicioForm()
    return render(request, 'envios/pagar_servicio.html', {'form': form})

def ver_historial(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    transacciones = usuario.transacciones.all().order_by('-fecha')
    return render(request, 'envios/historial.html', {'usuario': usuario, 'transacciones': transacciones})

# Vista para el gráfico usando Chart.js
def ver_grafico(request):
    return render(request, 'envios/ver_grafico.html')

def datos_grafico(request):
    usuarios = Usuario.objects.all()
    data = {
        'usuarios': [u.nombre for u in usuarios],
        'saldos': [float(u.saldo) for u in usuarios]
    }
    return JsonResponse(data)

