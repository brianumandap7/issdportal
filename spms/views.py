from core.django_helpers import helpers_crudjsn, helpers_string
from core.forms import UtilForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .models import CBSPerformance
from account.forms import UserBasicInfoForm


#============================================================================================
def performance_management(request):
    #CBSPerformance

    emp_list = CBSPerformance.objects.using('dospms').all().order_by('RateeName')
    emp_list = emp_list.filter(FiscalYear=2021,MotherUnitID=7)
    #emp_list = list(emp_list.values())
    context = {'emplist': emp_list } 

    return render(request, 'spms/performance_mgt.html',context)
#============================================================================================
#============================================================================================
@login_required(login_url='/')
def performance_modal(request):
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
                    summaryrpt = get_object_or_404(CBSPerformance.objects.using('docentral'), pk=ItemID)
                    form = UserBasicInfoForm(instance=summaryrpt)
                    context = {'utils':utils,'months': months,'form': form}
                    return render(request, 'account/performance_modal.html',context)
                except CBSPerformance.DoesNotExist:
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
                return render(request, 'account/performance_modal.html',context)
        else:
            # Handle non-AJAX POST requests gracefully
            return HttpResponse("This view only processes AJAX requests.", status=400)
#============================================================================================
#============================================================================================
@login_required(login_url='/')
def performance_details(request):
    return render(request, 'spms/performance_details.html')
#============================================================================================
@login_required(login_url='/')
def monitoringtool(request):
    return render(request, 'spms/monitoring_tool.html')
#============================================================================================