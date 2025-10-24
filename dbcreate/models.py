from time import strptime
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Roles(models.Model):
	Role_id = models.AutoField(primary_key=True)
	Role = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.Role

class Genders(models.Model):
	Gender_id = models.AutoField(primary_key=True)
	Gender = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.Gender

class Responder_tbl(models.Model):
	Responder_id = models.AutoField(primary_key=True)
	Resp = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'responder', null = True, blank = True)
	Gender = models.ForeignKey(Genders, on_delete = models.CASCADE, related_name = 'gender', null = True, blank = True)
	Roles = models.ManyToManyField(Roles, related_name='resroles', blank=True)

	def __str__(self):
		return str(self.Resp)

class Classification_tbl(models.Model):
	Classification_id = models.AutoField(primary_key=True)
	Classification = models.CharField(max_length=255, blank=True, null=True)
	Description = models.TextField(blank = True, null = True)

	def __str__(self):
		return self.Classification

class Severity_tbl(models.Model):
	Serverity_id = models.AutoField(primary_key=True)
	Severity = models.CharField(max_length=255, blank=True, null=True)
	Description = models.TextField(blank = True, null = True)

	def __str__(self):
		return self.Severity

class TLP_tbl(models.Model):
	TLP_id = models.AutoField(primary_key=True)
	TLP = models.CharField(max_length=255, blank=True, null=True)
	Description = models.TextField(blank = True, null = True) 

	def __str__(self):
		return self.TLP

class Ticket_tbl(models.Model):
	Ticket_id = models.AutoField(primary_key=True)
	Ticket_number = models.CharField(max_length=255, blank=True, null=True)
	Classification = models.ForeignKey(Classification_tbl, on_delete = models.CASCADE, related_name = 'ticket_classification', null = True, blank = True)
	Severity = models.ForeignKey(Severity_tbl, on_delete = models.CASCADE, related_name = 'ticket_severity', null = True, blank = True)
	Score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], null= True, blank = True)
	TLP = models.ForeignKey(TLP_tbl, on_delete = models.CASCADE, related_name = 'ticket_tlp', null = True, blank = True)
	Vulnerability = models.TextField(null=True, blank=True)
	Description = models.TextField(null=True, blank=True)
	Recommendations = models.TextField(null=True, blank=True)
	file_reference = models.FileField(upload_to='uploads/', null= True, blank = True)
	file_enc = models.CharField(max_length=255, blank=True, null=True)
	Responder = models.ForeignKey(Responder_tbl, on_delete=models.CASCADE, related_name = 'assigned_responder', null= True, blank = True)
	acknowledged_by = models.ForeignKey(Responder_tbl, on_delete=models.CASCADE, related_name = 'acknowledged_by', null= True, blank = True)

	def __str__(self):
		return self.Ticket_number

class Status_tbl(models.Model):
	Status_id = models.AutoField(primary_key=True)
	Status = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.Status

class IR_tbl(models.Model):
	IR_id = models.AutoField(primary_key=True)
	Ticket = models.ForeignKey(Ticket_tbl, on_delete=models.CASCADE, null = True, blank = True, related_name = "Ticket")
	Actions_taken = models.TextField(null=True, blank=True)
	Impact = models.TextField(null=True, blank=True)
	Root_cause = models.TextField(null=True, blank=True)
	Lessons_learned = models.TextField(null=True, blank=True)
	Status = models.ForeignKey(Status_tbl, on_delete=models.CASCADE, null = True, blank = True, related_name = "TStatus")

	def __str__(self):
		return self.Ticket