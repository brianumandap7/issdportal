from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from dbcreate.models import Responder_tbl, Ticket_tbl, IR_tbl
from .forms import TicketForm, AdvForm
from django.db.models import Q

# Create your views here.

def cs(request):
	# --- Handle Ticket Form ---
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cs')  # reload same page after saving
        form1 = AdvForm(request.POST, request.FILES)
        if form1.is_valid():
            form1.save()
            return redirect('cs')  # reload same page after saving
    else:
        form = TicketForm()
        form1 = AdvForm()
		
    context = {
		'workbench': Ticket_tbl.objects.filter(Classification__Classification = "Workbench").count(),
		'vulnerabilities': Ticket_tbl.objects.filter(Classification__Classification = "Threat").count(),
		'sonar': Ticket_tbl.objects.filter(Classification__Classification = "Project Sonar").count(),
		'advisories': Ticket_tbl.objects.filter(Classification__Classification = "Advisory").count(),

		'total': Ticket_tbl.objects.exclude(Classification__Classification = "Advisory").count(),
		'unassigned': Ticket_tbl.objects.exclude(Classification__Classification = "Advisory").filter(Responder = None).count(), #revise in where clause
		'investigation': Ticket_tbl.objects.exclude(Responder__isnull=True).count(),
		'resolved': IR_tbl.objects.filter(Status__Status = "Resolved").count(), #revise in where clause

		'form': form,
		'form1': form1,
		'tdata': Ticket_tbl.objects.exclude(Classification__Classification="Advisory"),
		'tdata1': Ticket_tbl.objects.filter(Classification__Classification="Advisory"),
	}

    return render(request, 'cs/cs.html', context)