from django.db import models

#==============================================================================================================
class UtilOfficeDivision(models.Model): 
    DivisionName = models.CharField(max_length=255)
    CodeName = models.CharField(max_length=10)

    class Meta:
        managed = False  # Table already exists
        db_table = 'UtilOfficeDivision'

    def __str__(self):
        return self.DivisionName
#==============================================================================================================
class UtilDivisionSectionUnit(models.Model): 
    DivisionID = models.IntegerField(null=True, blank=True)
    SectionUnitName = models.CharField(max_length=255)
    CodeName = models.CharField(max_length=10)

    class Meta:
        managed = False  # Table already exists
        db_table = 'UtilDivisionSectionUnit'

    def __str__(self):
        return self.SectionUnitName
#==============================================================================================================
class UtilSalaryGrade(models.Model): 
    SalaryGrade = models.CharField(max_length=50)
    StepOne = models.IntegerField(null=True, blank=True)
    StepTwo = models.IntegerField(null=True, blank=True)
    StepThree = models.IntegerField(null=True, blank=True)
    StepFour = models.IntegerField(null=True, blank=True)
    StepFive = models.IntegerField(null=True, blank=True)
    StepSix = models.IntegerField(null=True, blank=True)
    StepSeven = models.IntegerField(null=True, blank=True)
    StepEight = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False  # Table already exists
        db_table = 'UtilSalaryGrade'

    def __str__(self):
        return self.SalaryGrade
#==============================================================================================================
class UtilSalaryStep(models.Model):
    StepName = models.CharField(max_length=50)
    ColoumnName = models.CharField(max_length=50)

    class Meta:
        managed = False  # Table already exists
        db_table = 'UtilSalaryStep'

    def __str__(self):
        return self.StepName
#==============================================================================================================
class UtilDesignation(models.Model): 
    PositionName = models.CharField(max_length=255)

    class Meta:
        managed = False  # Table already exists
        db_table = 'UtilDesignation'

    def __str__(self):
        return self.PositionName
#==============================================================================================================
