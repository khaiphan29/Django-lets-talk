from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #or you may give a list of attr of the Model
        exclude = ['host', 'participants']