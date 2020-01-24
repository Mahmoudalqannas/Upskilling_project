from django import forms
from .models import CheckoutModel
from django.forms import ModelForm


class CheckoutForm(ModelForm):

    class Meta:
        model = CheckoutModel
        exclude = ['user']
