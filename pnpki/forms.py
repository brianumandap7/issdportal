from django import forms
from .models import Application, SummaryReport

#==================================================================================================
# JASB STARTS
class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['FirstName','MiddleName','LastName','GenderID','NationalityID','BirthDate','TaxIDNumber',
                  'OrgAgencyCompany','OrgUnitDeptDiv','HouseUnitNumber','Street','Barangay','MunicipalityCity','ProvinceState',
                  'ZipCode','MobileNumber','EmailAddress','TermServiceID']#,'PassportPhoto'],'StatusID'
        
        #fields = '__all__'
#==================================================================================================
from .models import UtilGender, Country, Province, CityMun, Barangay, RequiredDocs
#==================================================================================================
class SelectionForm(forms.Form):
    GenderType = forms.ModelChoiceField(queryset=UtilGender.objects.using('docentral').all(),empty_label=None,required=True,to_field_name='id')
    RequiredID = forms.ModelChoiceField(queryset=RequiredDocs.objects.using('docentral').all(),empty_label=None,required=True,to_field_name='id')
    CountryName = forms.ModelChoiceField(queryset=Country.objects.using('docentral').all().order_by('CountryName'),empty_label=None,required=True,to_field_name='id')
    provDesc = forms.ModelChoiceField(queryset=Province.objects.using('docentral').all().order_by('provDesc'),empty_label=None,required=True,to_field_name='provCode')
    citymunDesc = forms.ModelChoiceField(queryset=CityMun.objects.using('docentral').all(),empty_label=None,required=True,to_field_name='citymunCode')
    brgyDesc = forms.ModelChoiceField(queryset=Barangay.objects.using('docentral').all(),empty_label=None,required=True,to_field_name='brgyCode')
#==================================================================================================
class SummaryReportForm(forms.ModelForm):
    class Meta:
        model = SummaryReport
        fields = ['BatchNumber','DateStarts','DateEnds','ReportRemarks']
        #fields = '__all__'
#==================================================================================================
# JASB ENDS 
#==================================================================================================