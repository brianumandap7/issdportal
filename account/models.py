from django.db import models

#==============================================================================================================
class UserBasicInfo(models.Model):
    SystemID = models.CharField(max_length=20)
    UserID = models.IntegerField(null=True, blank=True)
    EmployeeNumber = models.CharField(max_length=20)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    MiddleName = models.CharField(max_length=100)
    MiddleInitial = models.CharField(max_length=20)
    ExtensionName = models.CharField(max_length=100)
    EmployeeName  = models.CharField(max_length=100)
    BirthDate = models.DateField()
    GenderID = models.CharField(max_length=100)
    DivisionID = models.IntegerField(null=True, blank=True)
    UnitSectionID = models.IntegerField(null=True, blank=True)
    PositionID = models.IntegerField(null=True, blank=True)
    SalaryGradeID = models.IntegerField(null=True, blank=True)
    SalaryStepID = models.IntegerField(null=True, blank=True)
    StatusID = models.IntegerField(null=True, blank=True)
    RemarksStatus = models.TextField(blank=True, null=True)
    TransDate = models.DateTimeField()
    StringID = models.CharField(max_length=100, unique=True, db_index=True, editable=False)

    class Meta:
        managed = False  # Table already exists
        db_table = 'UserBasicInfo'

    def __str__(self):
        return self.EmployeeNumber
#==============================================================================================================