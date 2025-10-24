from core.django_helpers import helpers_crudjsn, helpers_string
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import json

from django.http import JsonResponse #HttpResponse

from pnpki.models import ErrorLogs

#============================================================================================
# ERROR LOGS STARTS FROM PNPKI
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
            data = helpers_crudjsn.insert_item(ErrorLogs,data)
        else:
            data = {'response_advise': "No Found data..",'Notflix': 'Failure'}        

    return JsonResponse(data)
#============================================================================================
@login_required(login_url='/')
def logs_error_view(request):

    error = ErrorLogs.objects.all()
    error = error.order_by('id')
    
    return render(request, 'pnpki/logs_error_view.html', {'errors': error })
#============================================================================================
# ERROR LOGS ENDS
#============================================================================================
