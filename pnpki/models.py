from django.db import models
from datetime import date
from core.django_helpers import helpers_file

#==============================================================================================================
# JASB STARTS
#==============================================================================================================
class UtilStatusName(models.Model):
    id  = models.IntegerField(primary_key=True)
    Description = models.CharField(max_length=50)
    StatusCode = models.CharField(max_length=6)
    ClassName = models.CharField(max_length=50)

    class Meta:
        db_table = 'UtilStatusName'

    def __str__(self):
        return self.Description 
#==============================================================================================================
class Application(models.Model):

    ApplicationID = models.CharField(max_length=20)
    FirstName = models.CharField(max_length=100)
    MiddleName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    ExtensionName = models.CharField(max_length=100)
    GenderID = models.CharField(max_length=100)
    NationalityID = models.IntegerField(null=True, blank=True)
    BirthDate = models.DateField(null=True, blank=True)
    TaxIDNumber = models.CharField(max_length=50, blank=True)
    OrgAgencyCompany = models.CharField(max_length=200, blank=True)
    OrgUnitDeptDiv = models.CharField(max_length=200, blank=True)
    HouseUnitNumber = models.CharField(max_length=200, blank=True)
    Street = models.CharField(max_length=200, blank=True)
    Barangay = models.CharField(max_length=50, blank=True)
    MunicipalityCity = models.CharField(max_length=50, blank=True)
    ProvinceState = models.CharField(max_length=50, blank=True)
    ZipCode = models.CharField(max_length=5, blank=True)
    MobileNumber = models.CharField(max_length=50, blank=True)
    EmailAddress = models.CharField(max_length=100, blank=True)
    PassportPhoto = models.ImageField(upload_to="passport_photos/",validators=[helpers_file.validate_file_extension])
    SignatureImage = models.ImageField(upload_to='signatures/',validators=[helpers_file.validate_file_extension])
    TermServiceID = models.IntegerField(null=True, blank=True)
    StatusID = models.IntegerField(null=True, blank=True)
    #StatusID = models.ForeignKey(UtilStatusName, on_delete=models.CASCADE,db_column='StatusID')
    ApplicationDate = models.DateField()
    ApproveDate = models.DateField()
    SubmittedDate = models.DateField()
    TransDate = models.DateTimeField()
    StringID = models.CharField(max_length=100, unique=True, db_index=True, editable=False)

    class Meta:
        managed = False  # Table already exists
        db_table = 'Application'

    #def save(self, *args, **kwargs):
    #    self.full_clean()   # ✅ ensures validators always run
    #    super().save(*args, **kwargs)
    def __str__(self):
        return self.ApplicationID
#==============================================================================================================
class Attachment(models.Model):
    ApplicationID =  models.CharField(max_length=20)
    RequiredID = models.IntegerField(null=True, blank=True)
    AttachedFiles = models.ImageField(upload_to="attached_files/")
    TransDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False  # Table already exists
        db_table = 'Attachment'

    def __str__(self):
        return self.ApplicationID
#==============================================================================================================
class SummaryReport(models.Model):
    id = models.IntegerField(primary_key=True)
    ReportID = models.CharField(max_length=20)
    BatchNumber = models.CharField(max_length=100)
    DateStarts = models.DateField()
    DateEnds = models.DateField()
    SubmittedDate = models.DateField()
    ReportRemarks = models.TextField(
        blank=True,  # Allows the field to be left empty
        null=True    # Stores NULL in the database if empty
    )
    StatusID = models.IntegerField()
    TransDate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'SummaryReport'

    def __str__(self):
        return self.ReportID
#==============================================================================================================
# LOOK UP 
#==============================================================================================================    
class FrequencyClass(models.Model):
    id = models.AutoField(primary_key=True)
    Description = models.CharField(max_length=50)
    RangeStarts = models.CharField(max_length=10)
    RangeEnds   = models.CharField(max_length=10)
    StartsDate = models.CharField(max_length=6)
    EndsDate   = models.CharField(max_length=6)

    class Meta:
        managed = False  # Table already exists
        db_table = 'UtilFrequencyClass'

    def __str__(self):
        return self.Description
#==============================================================================================================    
class QuarterlyReport(models.Model):
    id = models.AutoField(primary_key=True)
    QuartID = models.CharField(max_length=20)
    Description = models.CharField(max_length=100)
    StartsDate = models.DateTimeField()
    EndsDate = models.DateTimeField()
    TransDate = models.DateTimeField()
    StatusID = models.IntegerField()
    StringID = models.CharField(max_length=100)
    
    class Meta:
        managed = False  # Table already exists
        db_table = 'QuarterlyReport'

    def __str__(self):
        return self.Description
#==============================================================================================================
# ADDRESS NATIONALITY
#==============================================================================================================
class UtilGender(models.Model):
    id = models.AutoField(primary_key=True)
    Description = models.CharField(max_length=30)

    class Meta:
        managed = False  # Table already exists
        db_table = 'UtilGender'

    def __str__(self):
        return self.Description
#==============================================================================================================
class Country(models.Model):
    id  = models.IntegerField(primary_key=True)
    CountryName  = models.CharField(max_length=255)
    NiceName  = models.CharField(max_length=255)
    numcode = models.CharField(max_length=5)
    
    class Meta:
        db_table = 'UtilRefCountry'

    def __str__(self):
        return self.NiceName
#==============================================================================================================    
class Province(models.Model):
    psgcCode = models.CharField(max_length=255, primary_key=True)#models.CharField(max_length=255)
    provDesc = models.TextField()
    regCode  = models.CharField(max_length=255)
    provCode = models.CharField(max_length=255)
    DefaultLogo = models.CharField(max_length=255, null = True, blank = True)

    class Meta:
        db_table = 'UtilRefProvince'

    def __str__(self):
        return self.provDesc
#==============================================================================================================
class CityMun(models.Model):
    psgcCode = models.CharField(max_length=255, primary_key=True)
    citymunDesc = models.TextField()
    regDesc  = models.CharField(max_length=255)
    provCode = models.CharField(max_length=255)
    citymunCode = models.CharField(max_length=255)
    DefaultLogo = models.CharField(max_length=255, null = True, blank = True)
    #province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities")
    
    class Meta:
        db_table = 'UtilRefCityMun'

    def __str__(self):
        return self.citymunDesc
#==============================================================================================================
class Barangay(models.Model):
    brgyCode = models.CharField(max_length=255, primary_key=True, null = False, blank = True)
    brgyDesc = models.TextField(null = True, blank = True)
    regCode  = models.CharField(max_length=255, null = True, blank = True)
    provCode = models.CharField(max_length=255, default='')
    citymunCode = models.CharField(max_length=255, null = True, blank = True)
    DefaultLogo = models.CharField(max_length=255, null = True, blank = True)
    #city = models.ForeignKey(CityMun, on_delete=models.CASCADE, related_name="barangays")
    #name = models.CharField(max_length=100)

    class Meta:
        db_table = 'UtilRefBarangay'

    def __str__(self):
        return self.brgyDesc
#==============================================================================================================
class RequiredDocs(models.Model):
    id  = models.IntegerField(primary_key=True)
    ClassID = models.IntegerField(null=True, blank=True)
    Description = models.CharField(max_length=255)
    
    class Meta:
        managed = False  # Table already exists
        db_table = 'UtilRequiredDocs'

    def __str__(self):
        return self.Description
#==============================================================================================================
# PLAN TO MOVE TO CODE APP
#==============================================================================================================
class ErrorLogs(models.Model):
    id  = models.IntegerField(primary_key=True)
    UserID  = models.CharField(max_length=50)
    TransactionID  = models.CharField(max_length=50)
    UriSegmentLoc = models.CharField(max_length=200)
    details = models.TextField()
    log = models.TextField()
    TransDate = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'logs_error'

    def __str__(self):
        return self.NiceName
#==============================================================================================================
