# Importing libraries
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Creating a form of registration
class RegistrationForm(UserCreationForm):
    # Fields of registration form
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    # Defining fields
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

    # Override function to create a user
    def save(self, commit=True):
        user = super(RegistrationForm, self).save()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


# Creating a form for order
class OrderForm(forms.Form):
    # Required fields of order form
    phone = forms.CharField(required=True)
    buy_type = forms.ChoiceField(widget=forms.Select(), choices=([('Pickup', 'Pickup'), ('Delivery', 'Delivery')]))
    address = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)

