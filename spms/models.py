from django.db import models

#==============================================================================================================
class CBSPerformance(models.Model):
    PerformanceID = models.CharField(max_length=20)
    FiscalYear = models.IntegerField(null=True, blank=True)
    DateStart = models.DateField()
    DateEnds = models.DateField()
    PerformanceDate = models.DateField()
    RatingPeriod = models.IntegerField(null=True, blank=True)
    MFOCommonID = models.IntegerField(null=True, blank=True)
    PerformanceTypeID = models.IntegerField(null=True, blank=True)
    FinalRating = models.DecimalField(max_digits=10, decimal_places=3)
    MotherUnitID = models.IntegerField(null=True, blank=True)
    DivisionUnitID = models.IntegerField(null=True, blank=True)
    PositionID = models.IntegerField(null=True, blank=True)
    RateeID = models.BigIntegerField()
    RateeLastName = models.TextField()
    RateeName = models.TextField()
    RaterID = models.BigIntegerField()
    RaterName = models.TextField()
    ApproverID = models.BigIntegerField()
    ApproverName = models.TextField()
    OfficeHeadID = models.BigIntegerField()
    OfficeHeadName = models.TextField()
    RaterApproverID = models.BigIntegerField()
    EncodedID = models.BigIntegerField()
    CommitmentMessage = models.TextField()
    PerformanceRemarks = models.TextField()
    TransDate = models.DateTimeField()
    StatusID = models.IntegerField(null=True, blank=True)
    StringID = models.CharField(max_length=100, unique=True, db_index=True, editable=False)

    class Meta:
        managed = False  # Table already exists
        db_table = 'CBSPerformance'

    def __str__(self):
        return self.PerformanceID
#==============================================================================================================