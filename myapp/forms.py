from django import forms
from django.contrib.auth.models import User
from .models import Node,TimeVolume

class RootForm(forms.ModelForm):
	class Meta:
		model = Node
		fields = ["name","age","actual_state"]

class NodeForm(forms.ModelForm):
	class Meta:
		model = Node
		fields = ["name","parent","date","tumor","anatomic_pathology","tumor_markers","site","position","treatment"]

class TableForm(forms.ModelForm):
	class Meta:
		model = TimeVolume
		fields = ["time","volume","node"]

