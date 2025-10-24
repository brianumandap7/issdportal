from core.django_helpers import helpers_crudjsn, helpers_string
from core.forms import UtilForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .models import UserBasicInfo
from .forms import UserBasicInfoForm

#============================================================================================

from django.contrib.auth.forms import UserCreationForm
from dbcreate.models import Responder_tbl
from dbcreate.models import User

#============================================================================================
# JASB STARTS
#============================================================================================
@login_required(login_url='/')
def employee_management(request):
    return render(request, 'account/employee_panel.html')
#============================================================================================
@login_required(login_url='/')
def employee_modal(request):
    import calendar
    if request.method == "POST":
        # Check for AJAX request using the modern method
        is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        months = [(f'{i:02}', calendar.month_name[i].upper()) for i in range(1, 13)]
        utils = UtilForm()
        if is_ajax_request:
            ItemID = request.POST.get("ItemID")
            if ItemID:
                try:
                    # Retrieve object and specify the database in one call
                    summaryrpt = get_object_or_404(UserBasicInfo.objects.using('docentral'), pk=ItemID)
                    form = UserBasicInfoForm(instance=summaryrpt)
                    context = {'utils':utils,'months': months,'form': form}
                    return render(request, 'account/employee_modal.html',context)
                except UserBasicInfo.DoesNotExist:
                    # Handle the case where the item doesn't exist
                    return JsonResponse({'error': 'Item not found'}, status=404)
            else:
                form = UserBasicInfoForm()
                # Generate a code and assign it to the form instance.
                # This is for display purposes on the initial load.
                if not form.instance.SystemID:
                    form.instance.id = ''
                    form.instance.SystemID = helpers_string.GenerateCode(11)
                #return JsonResponse({'error': 'ItemID is missing'}, status=400)
                context = {'utils':utils,'months': months,'form': form}
                return render(request, 'account/employee_modal.html',context)
        else:
            # Handle non-AJAX POST requests gracefully
            return HttpResponse("This view only processes AJAX requests.", status=400)
#============================================================================================
# SAVE EMPLOYEE STARTS
#============================================================================================
@login_required(login_url='/')
@csrf_exempt
def employee_create(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'response_advise': 'Invalid request method.'}, status=400)
    
    # Assuming the form data is coming from a standard POST request, not JSON
    form = UserBasicInfoForm(request.POST, request.FILES) 
    if not form.is_valid():
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    cleaned_data = form.cleaned_data

    fname = cleaned_data.get('FirstName', '')
    mname = cleaned_data.get('MiddleName', '')
    lname = cleaned_data.get('LastName', '')
    xname = cleaned_data.get('ExtensionName', '')
    
    username = helpers_string.GetUsernameLower(fname, mname, lname, xname)
    email = f"{username}@dotr.gov.ph"
    password = username # Consider using a more secure temporary password logic
    
    # Check if a user with this username already exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'Notflix':'Failure', 'response_advise': 'A user with this username already exists.'}, status=400)
    
    try:
        # Create auth_user only once, using keyword arguments for optional fields
        new_user = User.objects.create_user(username=username,email=email,password=password,first_name=fname,last_name=lname)
        # Build the hash source string
        hash_source = f"{fname}|{mname}|{lname}|{xname}|{cleaned_data.get('Gender', '')}|{cleaned_data.get('BirthDate', '')}"
        unique_hash = helpers_string.GetHash(hash_source)
        
        # Assign generated values to cleaned_data
        cleaned_data['UserID'] = new_user.id
        cleaned_data['SystemID'] = helpers_string.GenerateCode(11)
        cleaned_data['MiddleInitial'] = helpers_string.GetInitialsUpper(mname)
        cleaned_data['EmployeeName'] = helpers_string.GetAlphaName(fname, mname, lname, xname)
        cleaned_data['BirthDate'] = timezone.now().date() 
        cleaned_data['GenderID'] = 1 
        cleaned_data['SalaryStepID'] = 1 
        cleaned_data['StatusID'] = 1
        cleaned_data['TransDate'] = timezone.now()
        cleaned_data['StringID'] = unique_hash

        # Insert item and get the created object
        response = helpers_crudjsn.check_insert(UserBasicInfo, cleaned_data,'docentral')
        if not response.get('success'):
            return JsonResponse(response, status=400)
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'response_advise': f'An unexpected error occurred: {e}'}, status=500)

    return JsonResponse(response)
#============================================================================================
# SAVE EMPLOYEE ENDS
#============================================================================================
def employee_list(request):
    if request.method == 'POST':
        #SDateFrom = request.POST.get("SearchDateFrom")
        #SDateEnds = request.POST.get("SearchDateEnds")
        #SStatusID = request.POST.get("StatusID")

        emp_list = UserBasicInfo.objects.using('docentral').all().order_by('EmployeeName')
        emp_list = list(emp_list.values())
    context = {'emplist': emp_list }
        
    return JsonResponse(context)
#============================================================================================
# JASB ENDS
#============================================================================================
# TESTING
#============================================================================================
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})

def profile(request):
	responder = Responder_tbl.objects.filter(Resp=request.user).first()
	responder1 = Responder_tbl.objects.filter(Resp=request.user)
	query = {
        "roles": responder.Roles.all() if responder else [],
        "responder": responder,
		"responder1": responder1,
		'udet': User.objects.filter(username = request.user),
	}
	return render(request, 'users/profile.html', query)
#============================================================================================