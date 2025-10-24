from django import forms
from .models import UserBasicInfo

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
#==================================================================================================
# JASB STARTS
class UserBasicInfoForm(forms.ModelForm):
    class Meta:
        model = UserBasicInfo
        fields = ['FirstName','MiddleName','LastName','DivisionID','UnitSectionID','PositionID','SalaryGradeID','RemarksStatus']
        
        #fields = '__all__'
#==================================================================================================
# JASB ENDS
#==================================================================================================
class CustomAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']
    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'off'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'})
#==================================================================================================