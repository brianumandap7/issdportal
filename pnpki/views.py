from core.django_helpers import helpers, helpers_crudjsn, helpers_string, helpers_file, helpers_img, helpers_email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from django.http import HttpResponse, JsonResponse

from .models import Application, Attachment, SummaryReport, FrequencyClass, QuarterlyReport, ErrorLogs, RequiredDocs, UtilStatusName, UtilGender, Country, Province, CityMun, Barangay
from .forms import ApplicantForm, SelectionForm, SummaryReportForm

import os, calendar, hashlib, base64, json, PIL, PIL.Image
from django.core.files.base import ContentFile
from django.utils import timezone
from django.urls import reverse
from urllib.parse import urlencode
from uuid import uuid4

from django.db.models import Count

#============================================================================================
# JASB STARTS
#============================================================================================
def load_cities(request):
    province_id = request.GET.get("province_id")
    cities = CityMun.objects.using('docentral').filter(provCode=province_id).order_by("citymunDesc")
    return JsonResponse(list(cities.values("citymunCode", "citymunDesc")), safe=False)
def load_barangays(request):
    city_id = request.GET.get("city_id")
    barangays = Barangay.objects.using('docentral').filter(citymunCode=city_id).order_by("brgyDesc")
    return JsonResponse(list(barangays.values("brgyCode", "brgyDesc")), safe=False)
#============================================================================================
def applicant_form(request):
    form = SelectionForm()
    return render(request, 'pnpki/application_form.html',{"form": form})
#============================================================================================
# SAVE APPLICATION
#============================================================================================
def applicant_save(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'response_advise': 'Invalid request method.'}, status=400)

    form = ApplicantForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    try:
        # Prepare data from form.cleaned_data (the validated source)
        data = form.cleaned_data
        
        # Override fields with corrected or generated data
        data['ApplicationID'] = helpers_string.GenerateCode(11)
        data['TransDate'] = timezone.now() 
        data['ApplicationDate'] = timezone.now().date() 
        data['StatusID'] = 1#UtilStatusName.objects.using('docentral').get(pk=1)

        # Hashing logic (using cleaned_data)
        fname = data.get('FirstName', '')
        mname = data.get('MiddleName', '')
        lname = data.get('LastName', '')
        xname = data.get('ExtensionName', '') # Will be cleaned by form or handled below
        gender = data.get('GenderID', '')
        dob = data.get('BirthDate', '')
        hash_source = f"{fname}|{mname}|{lname}|{xname}|{gender}|{dob}"
        unique_hash = hashlib.sha256(hash_source.encode('utf-8')).hexdigest()
        data['StringID'] = unique_hash

        # Process Passport Photo
        pass_port = request.FILES.get('PassportPhoto')
        if pass_port:
            response = helpers_file.validate_file_extension(pass_port)
            if not response.get('success'):
                return JsonResponse(response, status=400)
            
            ext = os.path.splitext(pass_port.name)[-1]
            new_filename = f'{uuid4().hex}{ext}'
            pass_port.name = new_filename
            data['PassportPhoto'] = pass_port
        else:
            data['PassportPhoto'] = None
        
        # Process Signature Image
        signature_data = request.POST.get('SignatureImage')
        if signature_data:
            format, imgstr = signature_data.split(';base64,') 
            ext = format.split('/')[-1]
            file_data = ContentFile(base64.b64decode(imgstr), name=f"{uuid4().hex}.{ext}")
            data['SignatureImage'] = file_data
        else:
            data['SignatureImage'] = None

        # Insert item and get the created object
        response = helpers_crudjsn.check_insert(Application, data,'dopnpki')
        if not response.get('success'):
            return JsonResponse(response, status=400)
        
        pk_value = response['item_id']
        created_application = Application.objects.using('dopnpki').get(pk=pk_value)

        # Handle Attached Files
        attached_file = request.FILES.get('AttachedFiles')
        RequiredID = request.POST.get('RequiredID')
        if attached_file:
            ext = os.path.splitext(attached_file.name)[-1]
            new_filename = f'{uuid4().hex}{ext}'
            Attachment.objects.using('dopnpki').create(
                ApplicationID=created_application.ApplicationID,
                RequiredID=RequiredID,
                AttachedFiles=attached_file
            )

        # Image resizing (now safer)
        if created_application.PassportPhoto:
            file_path = created_application.PassportPhoto.path
            target_width = 413 
            target_height= 532
            
            img = PIL.Image.open(file_path)
            img = helpers_img.fix_image_orientation(img)
            img = helpers_img.crop_image(img, target_width, target_height)
            img = img.resize((target_width, target_height))
            img.save(file_path)
            
        # Email logic
        subject = "DOTR MISS PNPKI APPLICATION"
        message = "Hello, this is a test email."
        recipient_list = [created_application.EmailAddress]
        from_name = f"DOTR-MISS-PNPKI [{created_application.ApplicationID}]"
        from_email = "noreply@paymaster.ph"

        if helpers_email.send_custom_email_name(subject, message, recipient_list, from_email, from_name):
            response['email_status'] = "Email sent successfully!"
        else:
            response['email_status'] = "Failed to send email."

        # Construct and add the redirect URL
        base_url = reverse('certificate_view', kwargs={'pk': pk_value})
        query_string = urlencode({'appid': created_application.ApplicationID})
        response['redirect_url'] = f'{base_url}?{query_string}'
        response['app_id'] = created_application.ApplicationID

        return JsonResponse(response)

    except UtilStatusName.DoesNotExist:
        return JsonResponse({'status': 'error','response_advise': 'Invalid StatusID configuration.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error','response_advise': f'An unexpected error occurred: {e}'}, status=500)
#============================================================================================
# SAVE APPLICATION
#============================================================================================
@login_required(login_url='/')
def applicant_update(request):
    if request.method == "POST":
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            item_id = request.POST.get('id')
            data = form.cleaned_data

            try:
                data['StatusID'] = 2#UtilStatusName.objects.using('dopnpki').get(pk=2)
            except UtilStatusName.DoesNotExist:
                # Handle the case where the status ID is invalid
                return JsonResponse({'status': 'error','response_advise': 'Invalid StatusID provided.'}, status=400)

            data['TransDate'] = timezone.now()#??
            
            # Hash generation (as you already have)
            fname = data.get('FirstName', '')
            mname = data.get('MiddleName', '')
            lname = data.get('LastName', '')
            xname = data.get('ExtensionName', '')
            gender = data.get('GenderID', '')
            dob = data.get('BirthDate', '')
                    
            hash_source = f"{fname}|{mname}|{lname}|{xname}|{gender}|{dob}"
            unique_hash = hashlib.sha256(hash_source.encode('utf-8')).hexdigest()
            data['StringID'] = unique_hash

            # Pass the corrected `data` dictionary to the helper
            response = helpers_crudjsn.update_item(Application, item_id, data,'dopnpki')

            return JsonResponse(response)
        else:
            # The form is not valid; return the errors
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'response_advise': 'Invalid request method'}, status=400)  
#============================================================================================
# UPDATE APPLICATION ENDS
#============================================================================================
def certificate_view(request,pk):#,pk=None,appid=None
    ItemID = pk #request.GET.get("id")
    ApplicationID = request.GET.get("appid")
    #print(ItemID,':',ApplicationID)
    #if request.method == "POST":
        #if request.is_ajax() and Application.objects.filter(id=ItemID).count()>=1:
            #applicant = get_object_or_404(Application, pk=ItemID)
    applicant = get_object_or_404(Application.objects.using('dopnpki'), pk=ItemID,ApplicationID=ApplicationID)
    #applicant = applicant.filter(ApplicationID=ApplicationID)
    form = ApplicantForm(instance=applicant)
    attachment = Attachment.objects.using('dopnpki').all().filter(ApplicationID=ApplicationID)
    all_reqids = list(Attachment.objects.using('dopnpki').all().values_list('RequiredID', flat=True).filter(ApplicationID=ApplicationID))
    req_docs = RequiredDocs.objects.using('docentral').all()    
    reqiddoc = { 'req_docs': req_docs, 'all_reqids':all_reqids, 'cl_one':[1] , 'cl_two':[2], 'cl_tre':[3] }

    address = {
            'CountryName': helpers.GetValueDB('UtilRefCountry','id',form.instance.NationalityID,'CountryName','docentral'),
            'ProvName': helpers.GetValueDB('UtilRefProvince','provCode',form.instance.ProvinceState,'provDesc','docentral'),
            'CityMunname': helpers.GetValueDB('UtilRefCityMun','citymunCode',form.instance.MunicipalityCity,'citymunDesc','docentral'),
            'BrgyName': helpers.GetValueDB('UtilRefBarangay','brgyCode',form.instance.Barangay,'brgyDesc','docentral')
            }
    context = {'form':form, 'address':address, 'attachments':attachment, 'reqiddoc':reqiddoc}
    return render(request, 'pnpki/certificate_view.html',context)
#============================================================================================
@login_required(login_url='/')
def applicants(request):
    statusname = UtilStatusName.objects.using('docentral').all()
    return render(request, 'pnpki/applicants.html', {'statusname': statusname })
#============================================================================================
@login_required(login_url='/')
def applicants_list(request):
    from django.db.models import Count
    if request.method == 'POST':
        SDateFrom = request.POST.get("SearchDateFrom")
        SDateEnds = request.POST.get("SearchDateEnds")
        SStatusID = request.POST.get("StatusID")
        
    # 1. Fetch relevant status data from the 'docentral' database
    status_dict = {
        s.id: {'ClassName': s.ClassName, 'Description': s.Description, 'StatusCode': s.StatusCode}
        for s in UtilStatusName.objects.using('docentral').all()
    }

    # 2. Fetch applicant data from the 'dopnpki' database
    applicant_qs = Application.objects.using('dopnpki').all()
    
    # 3. Apply filters
    if SDateFrom:
        applicant_qs = applicant_qs.filter(ApplicationDate__gte=SDateFrom)
    if SDateEnds:
        applicant_qs = applicant_qs.filter(ApplicationDate__lte=SDateEnds)
    if SStatusID:
        applicant_qs = applicant_qs.filter(StatusID=SStatusID)
    
    # 4. Create a list of dictionaries with combined data
    applicant_list = []
    for applicant in applicant_qs.order_by('ApplicationDate').values():
        status_id = applicant.get('StatusID')
        status_info = status_dict.get(status_id)
        
        if status_info:
            applicant['StatusID__ClassName'] = status_info['ClassName']
            applicant['StatusID__Description'] = status_info['Description']
        else:
            applicant['StatusID__ClassName'] = 'Unknown'
            applicant['StatusID__Description'] = 'Unknown'
        
        # Manually select only the desired fields
        applicant_data = {
            'id': applicant.get('id'),
            'ApplicationID': applicant.get('ApplicationID'),
            'ApplicationDate': applicant.get('ApplicationDate'),
            'FirstName': applicant.get('FirstName'),
            'LastName': applicant.get('LastName'),
            'EmailAddress': applicant.get('EmailAddress'),
            'OrgAgencyCompany': applicant.get('OrgAgencyCompany'),
            'OrgUnitDeptDiv': applicant.get('OrgUnitDeptDiv'),
            'StatusID': applicant.get('StatusID'),
            'StatusID__ClassName': applicant.get('StatusID__ClassName'),
            'StatusID__Description': applicant.get('StatusID__Description'),
        }
        applicant_list.append(applicant_data)

    # 5. Aggregate counts (as shown in the previous answer)
    raw_counts = applicant_qs.values('StatusID').annotate(count=Count('StatusID'))
    count_per_status = {}
    for item in raw_counts:
        status_id = item['StatusID']
        count = item['count']
        status_info = status_dict.get(status_id)

        if status_info:
            count_per_status[status_info['StatusCode']] = count
    
    # 6. Render the template with the combined data
    context = {
        'count_per_status': count_per_status,
        'rtplist': applicant_list,
    }        
        
    return JsonResponse(context)
#============================================================================================
@login_required(login_url='/')
def applicant_view(request):
    ItemID = request.POST.get("ItemID")
    if request.method == "POST":
        if request.is_ajax() and Application.objects.using('dopnpki').filter(id=ItemID).count()>=1:
            #applicant = get_object_or_404(Application, pk=ItemID)
            queryset = Application.objects.using('dopnpki')
            applicant = get_object_or_404(queryset, pk=ItemID)
            form = ApplicantForm(instance=applicant)
            attachment = Attachment.objects.using('dopnpki').all().filter(ApplicationID=form.instance.ApplicationID)
            
            GenderName = UtilGender.objects.using('docentral').order_by("id")
            CountryName = Country.objects.using('docentral').order_by("id")
            ProvName = Province.objects.using('docentral').order_by("provDesc")
            CityName = CityMun.objects.using('docentral').filter(provCode=form.instance.ProvinceState).order_by("citymunDesc")
            BrgyName = Barangay.objects.using('docentral').filter(citymunCode=form.instance.MunicipalityCity).order_by("brgyDesc")
            select = {'GenderName':GenderName, 'BrgyName':BrgyName, 'CityName':CityName, 'ProvName':ProvName, 'CountryName':CountryName }
            
            address = {
            'GenderName': helpers.GetValueDB('UtilGender','id',form.instance.GenderID,'Description','docentral'),    
            'CountryName': helpers.GetValueDB('UtilRefCountry','id',form.instance.NationalityID,'CountryName','docentral'),
            'ProvName': helpers.GetValueDB('UtilRefProvince','provCode',form.instance.ProvinceState,'provDesc','docentral'),
            'CityMunname': helpers.GetValueDB('UtilRefCityMun','citymunCode',form.instance.MunicipalityCity,'citymunDesc','docentral'),
            'BrgyName': helpers.GetValueDB('UtilRefBarangay','brgyCode',form.instance.Barangay,'brgyDesc','docentral')
            }

    return render(request, 'pnpki/applicant_modal.html',{'form':form, 'select':select, 'address':address, 'attachments':attachment})
#============================================================================================
@login_required(login_url='/')
def remove_data(request):
    ItemID = request.POST.get("ItemID")
    ApplicationID = request.POST.get("TransID")
    if request.method == "POST":
        if request.is_ajax() and Application.objects.using('dopnpki').filter(id=ItemID).count()>=1:
            #applicant = get_object_or_404(Application, pk=ItemID)
            #applicant.delete()
            data = helpers_crudjsn.delete_item(Application,ItemID,'dopnpki')
            where_data = {'ApplicationID':ApplicationID}
            helpers_crudjsn.delete_where(Attachment, where_data,'dopnpki')
        else:
            data = {'response_advise': "No Found data..",'Notflix': 'Failure'}
    
    applicant = Application.objects.using('dopnpki').all()
    applicant = applicant.order_by('id')
    data['applicants'] = render_to_string('pnpki/applicants_list.html', {'applicants': applicant})

    return JsonResponse(data)
#============================================================================================
@login_required(login_url='/')
def approve_data(request):
    if request.method == "POST":
        # Check if it's an AJAX request (more compatible with modern Django)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            ItemID = request.POST.get("ItemID")
            ApproveDate = timezone.now().date() #timezone.now()

            try:
                # Retrieve the UtilStatusName instance for the 'approved' status
                # Using get_object_or_404 is a good practice
                status_instance = 4#get_object_or_404(UtilStatusName.objects.using('dopnpki'), pk=4)

                # Prepare the update data dictionary with the model instance
                data_to_update = {'StatusID': status_instance, 'ApproveDate': ApproveDate}

                # Call the update helper and get its response
                response = helpers_crudjsn.update_item(Application, ItemID, data_to_update,'dopnpki')

                # Handle success or failure from the update helper
                if response.get('success'):
                    # Success message
                    response['response_advise'] = "Application approved successfully."
                else:
                    # Specific error message from helper
                    response['response_advise'] = "Update failed: " + response.get('error', 'Unknown error')
                
            except UtilStatusName.DoesNotExist:
                # Handle the case where the approved status is not found
                response = {'response_advise': "Error: 'Approved' status not found.", 'Notflix': 'Failure'}
            except Exception as e:
                # Catch any other potential errors
                response = {'response_advise': f"An error occurred: {e}", 'Notflix': 'Failure'}

        else:
            response = {'response_advise': "Invalid request type. Must be AJAX.", 'Notflix': 'Failure'}
    else:
        response = {'response_advise': "Invalid request method.", 'Notflix': 'Failure'}

    # Retrieve and filter the applicants after the update has occurred
    DateFrom = timezone.now().date()
    applicants = Application.objects.using('dopnpki').all().filter(TransDate__gte=DateFrom).order_by('id')
    
    # Add the rendered HTML string to the response data
    response['applicants'] = render_to_string('pnpki/applicants_list.html', {'applicants': applicants})

    return JsonResponse(response)
#============================================================================================
@login_required(login_url='/')
def applicants_report(request):
    if request.method == 'POST':

        SDateFrom = request.POST.get("SearchDateFrom")
        SDateEnds = request.POST.get("SearchDateEnds")
        SStatusID = request.POST.get("StatusID")
        token = request.POST.get("csrfmiddlewaretoken")
        base_url = reverse('applicationreport')
        # Prepare the query string
        query_string = urlencode({'token':token,'datefrom': SDateFrom, 'dateends': SDateEnds, 'statusid':SStatusID})
        # Combine the base URL and the query string
        redirect_url = f'{base_url}?{query_string}'

        data = {'message': 'Success', 'status': 200, 'redirect_url':redirect_url}
        return JsonResponse(data) # Correct
            #return HttpResponse('Only POST requests allowed.')
    else:

        datefrom = request.GET.get("datefrom")
        dateends = request.GET.get("dateends")
        statusid = request.GET.get("statusid")

        ReportsCoverage = f"{datefrom} to {dateends}"
        
        apps =  Application.objects.using('dopnpki').all()
        if datefrom:
            apps = apps.filter(ApplicationDate__gte=datefrom)
        if dateends:
            apps = apps.filter(ApplicationDate__lte=dateends)
        if statusid:
            apps = apps.filter(StatusID=statusid)
        
        apps = apps.order_by('ApplicationDate')

    return render(request, 'pnpki/certificate_report.html', {'applicants': apps, 'ReportsCoverage':ReportsCoverage })
#============================================================================================
#
#============================================================================================
@login_required(login_url='/')
def dashboard(request):
    return render(request, "pnpki/dashboard.html")
#============================================================================================
#
#============================================================================================
# SUMMARY REPORTS
#============================================================================================
@login_required(login_url='/')
def summary_reports(request):
    
    summary = SummaryReport.objects.using('dopnpki').all()
    statusname = UtilStatusName.objects.using('docentral').all()
    context = {'summary':summary, 'statusname': statusname }

    return render(request, 'pnpki/summary_reports.html', context)
#============================================================================================
def modal_reports(request):
    import calendar
    if request.method == "POST":
        # Check for AJAX request using the modern method
        is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        months = [(f'{i:02}', calendar.month_name[i].upper()) for i in range(1, 13)]
        if is_ajax_request:
            ItemID = request.POST.get("ItemID")
            if ItemID:
                try:
                    # Retrieve object and specify the database in one call
                    summaryrpt = get_object_or_404(SummaryReport.objects.using('dopnpki'), pk=ItemID)
                    form = SummaryReportForm(instance=summaryrpt)
                    context = {'months': months,'form': form}
                    return render(request, 'pnpki/reports_modal.html',context)
                except SummaryReport.DoesNotExist:
                    # Handle the case where the item doesn't exist
                    return JsonResponse({'error': 'Item not found'}, status=404)
            else:
                form = SummaryReportForm()
                # Generate a code and assign it to the form instance.
                # This is for display purposes on the initial load.
                if not form.instance.ReportID:
                    form.instance.id = ''
                    form.instance.ReportID = helpers_string.GenerateCode(11)
                #return JsonResponse({'error': 'ItemID is missing'}, status=400)
                context = {'months': months,'form': form}
                return render(request, 'pnpki/reports_modal.html',context)
        else:
            # Handle non-AJAX POST requests gracefully
            return HttpResponse("This view only processes AJAX requests.", status=400)
#============================================================================================
from datetime import datetime
def create_reports(request):
    if request.method == "POST":
        is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if is_ajax_request:
            # Get the id separately, as it determines if we're updating or creating.
            item_id = request.POST.get("id")
            DateStarts = request.POST.get("DateStarts")
            DateEnds   = request.POST.get("DateEnds")

            SubmittedDate = timezone.now().date()
            TransDate   = timezone.now()
        
            # Determine if this is an update or a new creation
            if item_id:
                # This is an update: fetch the existing instance and bind it to the form.
                try:
                    instance = SummaryReport.objects.using('dopnpki').get(pk=item_id)
                except SummaryReport.DoesNotExist:
                    return JsonResponse({'response_advise': 'Record not found.', 'Notflix': 'Failure'}, status=404)
                
                form = SummaryReportForm(request.POST, instance=instance)
            else:
                # This is a new creation: create an unbound form.
                form = SummaryReportForm(request.POST)

            if form.is_valid():
                report_data = form.cleaned_data
                report_data.update({
                    'SubmittedDate': SubmittedDate,
                    'StatusID': 2,
                    'TransDate': TransDate,
                })
                # Add the ID to the data if it exists for the helper function.
                if item_id:
                    report_data['id'] = item_id
                
                # Convert date strings to date objects and extract the month.
                from_month = datetime.strptime(DateStarts, '%Y-%m-%d').date().month
                ends_month = datetime.strptime(DateEnds, '%Y-%m-%d').date().month
                ends_year = datetime.strptime(DateEnds, '%Y-%m-%d').date().year
                
                lookup_where = {'RangeStarts__gte':f"{from_month:02d}", 'RangeEnds__lte':f"{ends_month:02d}" }
                rslt = helpers.GetValue_ORM(FrequencyClass,lookup_where,'Description','docentral')
                starts_date = helpers.GetValue_ORM(FrequencyClass,lookup_where,'StartsDate','docentral')
                ends_date = helpers.GetValue_ORM(FrequencyClass,lookup_where,'EndsDate','docentral')
                
                QuartID = helpers_string.GenerateCode(11)
                Description = f"{rslt} {ends_year}"
                StartsDate = f"{ends_year}{starts_date}"
                EndsDate = f"{ends_year}{ends_date}"
                StringID = hashlib.sha256(Description.encode('utf-8')).hexdigest()
                
                quarts_data = {'QuartID': QuartID, 'Description':Description,'StartsDate':StartsDate,'EndsDate':EndsDate,'TransDate': timezone.now(),'StatusID':1,'StringID':StringID}
                
                where_data = {'Description':Description}
                #result = helpers_crudjsn.insert_update_where(QuarterlyReport, quarts_data, where_data,'dopnpki')
                result = helpers_crudjsn.check_insert(QuarterlyReport,quarts_data,'dopnpki')
                #check_and_update(QuarterlyReport, quarts_data, 'dopnpki')
                
                #=================================================
                rtplist_queryset = SummaryReport.objects.using('dopnpki').all().order_by('id')
                rtplist_data = list(rtplist_queryset.values())
                result['rtplist'] = rtplist_data

                result = helpers_crudjsn.check_and_update(SummaryReport, report_data, 'dopnpki')

                #====UPDATE APPLICATION====
                update_data = {'StatusID':5,'SubmittedDate': SubmittedDate,'TransDate': TransDate}
                where_data = {'StatusID':4, 'ApproveDate__gte': DateStarts, 'ApproveDate__lte' : DateEnds }
                helpers_crudjsn.update_item_where(Application, update_data, where_data,'dopnpki')
                #====UPDATE APPLICATION====

                return JsonResponse(result)
            else:
                return JsonResponse({'response_advise': 'Form validation failed', 'errors': form.errors, 'Notflix': 'Failure'}, status=400)
        else:
            return JsonResponse({'response_advise': 'Invalid request format or method', 'Notflix': 'Failure'}, status=400)

    return JsonResponse({'response_advise': 'Invalid request method', 'Notflix': 'Failure'}, status=405)
#============================================================================================
def get_summary_reports(request):
    if request.method == 'POST':
        # Retrieve form data, using .get() with a default of None
        s_date_from_str = request.POST.get("SearchDateFrom")
        s_date_ends_str = request.POST.get("SearchDateEnds")
        s_status_id_str = request.POST.get("StatusID")
        
        # 1. Fetch relevant status data from the 'docentral' database
        status_dict = {
            s.id: {'ClassName': s.ClassName, 'Description': s.Description, 'StatusCode': s.StatusCode}
            for s in UtilStatusName.objects.using('docentral').all()
        }

        # 2. Fetch applicant data from the 'dopnpki' database
        applicant_qs = Application.objects.using('dopnpki').all()
        
        # 3. Apply filters
        if s_date_from_str:
            try:
                s_date_from_date = datetime.strptime(s_date_from_str, '%Y-%m-%d').date()
                applicant_qs = applicant_qs.filter(ApplicationDate__gte=s_date_from_date)
            except (ValueError, TypeError):
                pass
        if s_date_ends_str:
            try:
                s_date_ends_date = datetime.strptime(s_date_ends_str, '%Y-%m-%d').date()
                applicant_qs = applicant_qs.filter(ApplicationDate__lte=s_date_ends_date)
            except (ValueError, TypeError):
                pass
        if s_status_id_str and s_status_id_str.isdigit():
            applicant_qs = applicant_qs.filter(StatusID=int(s_status_id_str))

        # 4. Aggregate applicant counts
        raw_counts = applicant_qs.values('StatusID').annotate(count=Count('StatusID'))
        count_per_status = {}
        for item in raw_counts:
            status_id = item['StatusID']
            count = item['count']
            status_info = status_dict.get(status_id)

            if status_info:
                count_per_status[status_info['StatusCode']] = count

        # ===================================================================================
        # 5. Process Summary Reports
        rtplist_queryset = SummaryReport.objects.using('dopnpki').all().order_by('DateStarts')
        if s_date_from_str:
            try:
                s_date_from_date = datetime.strptime(s_date_from_str, '%Y-%m-%d').date()
                rtplist_queryset = rtplist_queryset.filter(SubmittedDate__gte=s_date_from_date)
            except (ValueError, TypeError):
                pass
        if s_date_ends_str:
            try:
                s_date_ends_date = datetime.strptime(s_date_ends_str, '%Y-%m-%d').date()
                rtplist_queryset = rtplist_queryset.filter(SubmittedDate__lte=s_date_ends_date)
            except (ValueError, TypeError):
                pass
        
        rtplist = list(rtplist_queryset)
        
        # Determine date range from rtplist
        min_date = min(r.DateStarts for r in rtplist) if rtplist else None
        max_date = max(r.DateEnds for r in rtplist) if rtplist else None

        # Fetch applications based on ApproveDate and SubmittedDate
        applications_approved = []
        applications_submitted = []
        if min_date and max_date:
            applications_approved = Application.objects.using('dopnpki').filter(
                StatusID__lte=5,  # Only interested in approved status
                ApplicationDate__gte=min_date,
                ApplicationDate__lte=max_date,
            )
            applications_submitted = Application.objects.using('dopnpki').filter(
                StatusID=5,  # Only interested in submitted status
                SubmittedDate__gte=min_date,
                SubmittedDate__lte=max_date,
            )

        # Perform the "join" and counting in Python
        reports_with_counts = []
        for r in rtplist:
            count_approved = sum(1 for app in applications_approved if r.DateStarts <= app.ApplicationDate <= r.DateEnds)
            count_submitted = sum(1 for app in applications_submitted if r.DateStarts <= app.SubmittedDate <= r.DateEnds)
            BatchYear = r.DateStarts.year
            MonthName = calendar.month_name[int(r.BatchNumber)].upper()
            BatchNumber = f"{MonthName} {BatchYear}"

            re_submitted_cnt = count_approved - count_submitted
            reports_with_counts.append({
                'id': r.id,
                'ReportID': r.ReportID,
                'BatchNumber': BatchNumber,
                'SubmittedDate': r.SubmittedDate,
                'approved_cnt': count_approved,
                'submitted_cnt': count_submitted,
                're_submitted_cnt': re_submitted_cnt,
                'DateStarts':r.DateStarts,
                'DateEnds': r.DateEnds
            })
        
        rtplist_data = reports_with_counts

        # ===================================================================================
        # 6. Process Quarterly Reports
        rpt_quart = QuarterlyReport.objects.using('dopnpki').all().order_by('StartsDate')
        if s_date_from_str:
            try:
                s_date_from_date = datetime.strptime(s_date_from_str, '%Y-%m-%d').date()
                rpt_quart = rpt_quart.filter(TransDate__gte=s_date_from_date)
            except (ValueError, TypeError):
                pass
        if s_date_ends_str:
            try:
                s_date_ends_date = datetime.strptime(s_date_ends_str, '%Y-%m-%d').date()
                rpt_quart = rpt_quart.filter(TransDate__lte=s_date_ends_date)
            except (ValueError, TypeError):
                pass

        rpt_quart_list = []
        for qr in rpt_quart:
            qrt_cnt = SummaryReport.objects.using('dopnpki').filter(DateStarts__gte=qr.StartsDate, DateStarts__lte=qr.EndsDate).count()
            base_url = reverse('print-summary-rpts', kwargs={'pk': qr.id})
            query_string = urlencode({'quaid': qr.QuartID})
            print_view_url = f'{base_url}?{query_string}'
            rpt_quart_list.append({
                'id': qr.id,
                'QuartID': qr.QuartID,
                'Description': qr.Description,
                'qrt_cnt': qrt_cnt,
                'print_view_url': print_view_url
            })
        
        rptquart = rpt_quart_list
        
        # 7. Combine all data into a single dictionary and return as JSON
        final_data = {
            'count_per_status': count_per_status,
            'rtplist': rtplist_data,
            'rptquart': rptquart
        }
        
        return JsonResponse(final_data)

    return JsonResponse({'message': 'This endpoint only accepts POST requests'}, status=405)
#============================================================================================        
def print_summary_rpts(request,pk):
    ItemID  = pk #request.GET.get("id")
    QuartID = request.GET.get("quaid")
    
    #=============================================================
    filters = {'id':ItemID, 'QuartID':QuartID}
    QR = helpers.select_row(QuarterlyReport,'dopnpki',**filters)
    header_title = QR.Description #'1st Quarter of 2025'
    #=============================================================

    rtplist = SummaryReport.objects.using('dopnpki').all().order_by('DateStarts')
    rtplist = rtplist.filter(DateStarts__gte=QR.StartsDate)
    rtplist = rtplist.filter(DateEnds__lte=QR.EndsDate)
    #rtplist_queryset = rtplist_queryset.filter(StatusID=SStatusID)

    rtplist = list(rtplist)
    target_status_ids = [4, 5]
    min_date = min(r.DateStarts for r in rtplist) if rtplist else None
    max_date = max(r.DateEnds for r in rtplist) if rtplist else None

    # Fetch applications based on ApproveDate
    applications_approved = []
    if min_date and max_date:
        applications_approved = Application.objects.using('dopnpki').filter(
            StatusID__lte=5,  # Only interested in approved status
            ApplicationDate__gte=min_date,
            ApplicationDate__lte=max_date,
        )

    # Fetch applications based on SubmittedDate
    applications_submitted = []
    if min_date and max_date:
        applications_submitted = Application.objects.using('dopnpki').filter(
            StatusID=5,  # Only interested in submitted status
            SubmittedDate__gte=min_date,
            SubmittedDate__lte=max_date,
        )

    # Perform the "join" and counting in Python
    total_app_cnt = 0
    total_sub_cnt = 0
    total_res_cnt = 0
    reports_with_counts = []
    for r in rtplist:
        count_approved = 0
        count_submitted = 0

        BatchYear = r.DateStarts.year
        MonthName = calendar.month_name[int(r.BatchNumber)].upper()
        BatchNumber = f"{MonthName} {BatchYear}"

        for app in applications_approved:
            if r.DateStarts <= app.ApplicationDate <= r.DateEnds:
                count_approved += 1
        
        for app in applications_submitted:
            if r.DateStarts <= app.SubmittedDate <= r.DateEnds:
                count_submitted += 1

        re_submitted_cnt =  count_approved - count_submitted

        total_app_cnt += count_approved
        total_sub_cnt += count_submitted
        total_res_cnt += re_submitted_cnt
        reports_with_counts.append({
            'id': r.id,
            'BatchNumber': BatchNumber,
            'SubmittedDate': r.SubmittedDate,
            'approved_cnt': count_approved,
            'submitted_cnt': count_submitted,
            're_submitted_cnt': re_submitted_cnt,
        })
    
    context = {
        'reports': reports_with_counts,
        'target_status_ids': target_status_ids,
        'header_title':header_title,
        'total_app_cnt':total_app_cnt,
        'total_sub_cnt':total_sub_cnt,
        'total_res_cnt':total_res_cnt
    }
    
    return render(request, 'pnpki/reports_print.html', context)
#============================================================================================
@login_required(login_url='/')
def remove_summary(request):
    ItemID = request.POST.get("ItemID")
    ReportID = request.POST.get("TransID")
    if request.method == "POST":
        if request.is_ajax() and SummaryReport.objects.using('dopnpki').filter(id=ItemID).count()>=1:
            data = helpers_crudjsn.delete_item(SummaryReport,ItemID,'dopnpki')
            where_data = {'ReportID':ReportID}
            #helpers_crudjsn.delete_where(Attachment, where_data,'dopnpki')
        else:
            data = {'response_advise': "No Found data..",'Notflix': 'Failure'}

    return JsonResponse(data)
#============================================================================================
# SUMMARY REPORTS
#============================================================================================
#============================================================================================
# ERROR LOGS STARTS
#============================================================================================
def errorlogs(request):
    ItemID = request.POST.get("ItemID")
    TransID = request.POST.get("TransID")
    UriSegmentLoc = request.POST.get("UriSegmentLoc")
    tblname = request.POST.get("tblname")
    log = request.POST.get("log")
    TransactionID = helpers_string.GenerateCode(11)

    json_data_dict = {"tbl-name": tblname, "id": ItemID, "ApplicationID": TransID}
    json_data_string = json.dumps(json_data_dict)
    
    if request.method == "POST":
        if request.is_ajax():
            
            data = { 'UserID':request.user.id, 'TransactionID':TransactionID, 'UriSegmentLoc':UriSegmentLoc, 'details':json_data_string,  'log':log }
            print('data : ',data)
            data = helpers_crudjsn.insert_item(ErrorLogs,data,'docentral')
        else:
            data = {'response_advise': "No Found data..",'Notflix': 'Failure'}        

    return JsonResponse(data)
#============================================================================================
@login_required(login_url='/')
def logs_error_view(request):

    error = ErrorLogs.objects.using('docentral').all()
    error = error.order_by('id')
    
    return render(request, 'pnpki/logs_error_view.html', {'errors': error })
#============================================================================================
# ERROR LOGS ENDS
#============================================================================================
#============================================================================================
# TESTING
#============================================================================================
@login_required(login_url='/')
def homepage(request):
#    #return HttpResponse("Hellow Worlds! I'm Home.")
    return render(request, 'pnpki/home.html')
#============================================================================================
@login_required(login_url='/')
def about_page(request):
    #return HttpResponse("My About Page.")
    return render(request, 'pnpki/about.html')
#============================================================================================    
@login_required(login_url='/')
def base(request):
    #return HttpResponse("My Base Page.")
    #return render(request, 'base/lte_base.html')
    return render(request, 'base/lte_base.html')
def layout(request):
    #return HttpResponse("My Base Page.")
    #return render(request, 'base/lte_base.html')
    return render(request, 'base/note_form.html')
def consentagreement_view(request):
    return render(request, 'pnpki/ConsentAgreement.html')
#============================================================================================
# JASB ENDS
#============================================================================================