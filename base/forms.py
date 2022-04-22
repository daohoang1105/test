from django.forms import ModelForm
from .models import Room, User, Warranty
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username','email', 'password1','password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username','email', 'bio']

class WarrantyForm(ModelForm):
    class Meta:
        model = Warranty
        fields = '__all__'