#from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
#from django.conf.urls.static import static
#from pnpki.views import upload_file
from django.contrib.auth.decorators import login_required
from . import views

#from django.urls import path
#from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
#from . import views

#protected_patterns = [
#    path('pnpki/applicants', views.applicants, name='applicants'),                  #Application List
#]

urlpatterns = [
    
    # JASB STARTS
    path('dashboard', views.dashboard, name='dashboard'),
    path('pnpki/application', views.applicant_form, name='application'),   #pnpki/application        #Registration Form
    path('pnpki/applicants', views.applicants, name='applicants'),                  #Application List
    path('pnpki/applicationsave', views.applicant_save, name='applicationsave'),
    path('pnpki/applicantslist', views.applicants_list, name='applicationlist'),
    path('pnpki/applicationview', views.applicant_view, name='applicantview'),      #ModalView

    path('pnpki/remove_data', views.remove_data, name='data_remove'),               #Remove Application
    path('pnpki/approve_data', views.approve_data, name='data_approve'),            #Approve Application   
    path("ajax/load-cities", views.load_cities, name="ajax_load_cities"),           #Contact Details
    path("ajax/load-barangays/", views.load_barangays, name="ajax_load_barangays"), #Contact Details

    path('pnpki/<int:pk>/certificate', views.certificate_view, name='certificate_view'),
    path('pnpki/applicantsreport', views.applicants_report, name='applicationreport'),
    path('pnpki/consentagreement', views.consentagreement_view, name='consentagreement_view'),

    path('pnpki/applicationupdate', views.applicant_update, name='applicationupdate'),
    path('pnpki/summaryreports', views.summary_reports, name='summary-reports'),
    path('pnpki/createreports', views.create_reports, name='create-reports'),
    path('pnpki/modalreports', views.modal_reports, name='modal-reports'),
    path('pnpki/getsummaryreports', views.get_summary_reports, name='get-summary-reports'),

    path('pnpki/<int:pk>/printsummaryrpts', views.print_summary_rpts,name='print-summary-rpts'),
    #path('pnpki/printsummaryrpts', views.print_summary_rpts, name='print-summary-rpts'),

    path('pnpki/remove_summary', views.remove_summary, name='remove-summary'),               #Remove SupportSummary

    path('pnpki/errorlogs', views.errorlogs, name='errorlogs'),
    path('pnpki/viewerrorlogs', views.logs_error_view, name='errorlogsview'),

    path('pnpki/home',views.homepage,name='home_page'),
    path('pnpki/about',views.about_page,name='about_page'),
    path('base',views.base),

    #TESTING
    # JASB ENDS

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
