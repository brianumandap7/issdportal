from django import forms
from .models import UtilSalaryGrade, UtilSalaryStep, UtilOfficeDivision, UtilDivisionSectionUnit, UtilDesignation  #UtilGender, 
# JASB STARTS
#==================================================================================================
class UtilForm(forms.Form):
    #GenderType = forms.ModelChoiceField(queryset=UtilGender.objects.using('docentral').all().order_by('id'),empty_label=None,required=True,to_field_name='id')
    OfficeDiv = forms.ModelChoiceField(queryset=UtilOfficeDivision.objects.using('docentral').all().order_by('id'),empty_label=None,required=True,to_field_name='id')
    SectnUnit = forms.ModelChoiceField(queryset=UtilDivisionSectionUnit.objects.using('docentral').all().order_by('id'),empty_label=None,required=True,to_field_name='id')
    SalaryGrade = forms.ModelChoiceField(queryset=UtilSalaryGrade.objects.using('docentral').all().order_by('id'),empty_label=None,required=True,to_field_name='id')
    SalaryStep = forms.ModelChoiceField(queryset=UtilSalaryStep.objects.using('docentral').all().order_by('id'),empty_label=None,required=True,to_field_name='id')
    Designation = forms.ModelChoiceField(queryset=UtilDesignation.objects.using('docentral').all().order_by('PositionName'),empty_label=None,required=True,to_field_name='id')
#==================================================================================================