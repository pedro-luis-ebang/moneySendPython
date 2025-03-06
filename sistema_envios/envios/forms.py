from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'saldo']

class TransferenciaForm(forms.Form):
    remitente = forms.CharField(max_length=100, label="Remitente")
    receptor = forms.CharField(max_length=100, label="Receptor")
    monto = forms.DecimalField(max_digits=10, decimal_places=2, label="Monto")

class DepositoForm(forms.Form):
    usuario = forms.CharField(max_length=100, label="Usuario")
    monto = forms.DecimalField(max_digits=10, decimal_places=2, label="Monto")

class RetiroForm(forms.Form):
    usuario = forms.CharField(max_length=100, label="Usuario")
    monto = forms.DecimalField(max_digits=10, decimal_places=2, label="Monto")

class PagoServicioForm(forms.Form):
    usuario = forms.CharField(max_length=100, label="Usuario")
    servicio = forms.CharField(max_length=100, label="Servicio")
    monto = forms.DecimalField(max_digits=10, decimal_places=2, label="Monto")
