from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TrainSearchForm(forms.Form):
    source = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'From (e.g. Bangalore)'}))
    destination = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'To (e.g. Chennai)'}))
    journey_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))


class PassengerCountForm(forms.Form):
    num_passengers = forms.IntegerField(
        min_value=1, max_value=6, initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'max-width:120px'})
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
