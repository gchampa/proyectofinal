from django import forms


class VehiculoForms(forms.Form):
    mark = forms.CharField(max_length=40)
    model = forms.CharField(max_length=40)
    patent = forms.CharField(max_length=40)


class PropietarioForms(forms.Form):
    name = forms.CharField(max_length=40)
    lastname = forms.CharField(max_length=40)
    email = forms.EmailField()

class TallerForms(forms.Form):
    name = forms.CharField(max_length=40)
    address = forms.CharField(max_length=40)
    city=forms.CharField(max_length=40)

class MessagesForms(forms.Form):
    user = forms.CharField(max_length=40)
    mesg = forms.CharField(max_length=10000)
    #date = forms.DateField()