from django.db import models
from master_data.models import *
import uuid


# Create your models here.

PRE_ART_STATUS_CHOICES = (
    (1, 'Eligible but not Initiated on ART'),
    (2, 'Died'),
    (3, 'Opted out'),
    (4, 'Transfer Out'),
    (5, 'Initiated on ART'),
    (6, 'LFU before 31 Dec 2016'),
    (7, 'LFU after 1 Jan 2017')
)

ART_CARE_CHOICES = (
        (1, 'Alive on ART'),
        (2, 'Died'),
        (3, 'LFU after 1 Jan 2017'),
        (4, 'Stopped'),
        (5, 'MIS'),
        (6, 'Transfer Out'),
        (7, 'Opted out'),
        (8, 'LFU before 31 Dec 2016')
    )

HIV_REPORT_CHOICES=(
        (1, 'HIV-1'),
        (2, 'HIV-2'),
        (3, 'HIV-1 & 2'),
        (4, 'Update')
    )

ART_DIA_HYP = (
    (1, 'Pre-existing'),
    (2, 'Detected during treatment'),
    (3, 'No')
)    

class ArtRegistration(BaseContent):

    YES_NO_CHOICES=(
        (1,'NO'),
        (2,'YES')
    )

    YES_NO_FAMILY=(
        (1,'NO'),
        (2,'YES'),
        (3, 'Update')
    )
    TRANSFERRED_STATUS = (
        (1, 'PRE ART'),
        (2, 'On ART')
    )
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    art_center = models.ForeignKey(Boundary,on_delete=models.DO_NOTHING,related_name='art_center',null=True, blank=True)
    name_patient = models.CharField(max_length = 50, blank=False, null=False)
    date_registration = models.DateField()
    pre_art_no = models.CharField(max_length = 50,blank = False, null = False)
    status_in_pre_art_care = models.PositiveIntegerField(choices = PRE_ART_STATUS_CHOICES)
    death_date = models.DateField(blank=True,null=True)
    death_cause_uuid = models.CharField(max_length=250,blank = True, null = True)
    death_reason = models.TextField(blank=True,null=True)
    transferred_in = models.PositiveIntegerField(choices = YES_NO_CHOICES,null=True, blank=True)
    transfer_in_status = models.PositiveIntegerField(choices = TRANSFERRED_STATUS, null=True, blank=True)
    transferred_in_from_art = models.ForeignKey(Boundary, on_delete = models.DO_NOTHING, null=True, blank=True)
    date_art_initiation = models.DateField(null=True, blank = True)
    private_treatment_history =  models.PositiveIntegerField(choices = YES_NO_FAMILY)
    art_initiation_private_date = models.DateField(null=True, blank=True)
    hiv_test_confirmed_date = models.DateField()
    ictc_code = models.CharField(max_length=50, blank=False, null=False)
    pid_number = models.CharField(max_length=70, blank=False, null=False, unique=True)
    hiv_report = models.PositiveIntegerField(choices=HIV_REPORT_CHOICES)
    art_reg_no = models.CharField(max_length=50, blank=True, null=True)
    art_start_date = models.DateField(blank=True,null= True)
    art_care_status = models.PositiveIntegerField(choices = ART_CARE_CHOICES,blank=True,null=True)
    already_diagnosed_tb = models.PositiveIntegerField(choices = YES_NO_FAMILY)
    nikshay_id = models.BigIntegerField(unique=True, blank=True, null=True)
    samvaad_application_id = models.BigIntegerField(unique=True, blank=True, null=True)
    
    transfer_out_confirmation_data = models.DateField(blank=True, null=True)
    transferred_art_code = models.CharField(max_length=100, blank=True, null=True)
    disclosure_with_family = models.PositiveIntegerField(choices = YES_NO_FAMILY, blank=True, null=True)
    art_family_id = models.CharField(max_length=250, blank=True, null=True)
    imported      = models.BooleanField(default=False)
    art_reg_diabetes = models.PositiveIntegerField(choices = ART_DIA_HYP, blank=True, null=True)
    art_reg_hypertention = models.PositiveIntegerField(choices = ART_DIA_HYP, blank=True, null=True)
    
    def __str__(self):
        return self.name_patient



class ARTPatientLinkage(BaseContent):
    TRANSFERED_CHOICES = (
        (1, 'Transferred in'),
        (2, 'Transferred out')
    )
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(ArtRegistration,on_delete=models.DO_NOTHING,related_name='patient',null=True, blank=True)
    art_center = models.ForeignKey(Boundary,on_delete=models.DO_NOTHING,related_name='art_center_art_link')
    user = models.ForeignKey("auth.User",on_delete=models.DO_NOTHING)
    status = models.PositiveIntegerField(choices=TRANSFERED_CHOICES)

    def __str__(self):
        return self.patient.name_patient


class StatusHistory(models.Model):
    patient_name = models.ForeignKey(ArtRegistration, on_delete = models.DO_NOTHING, related_name = 'patient_name', null = True, blank = True)
    created_by = models.ForeignKey("auth.User",on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    present_status_in_pre_art_care = models.PositiveIntegerField(choices = PRE_ART_STATUS_CHOICES, blank=True, null=True)
    past_status_in_pre_art_care = models.PositiveIntegerField(choices = PRE_ART_STATUS_CHOICES, blank=True, null=True)
    present_status_art_care = models.PositiveIntegerField(choices = ART_CARE_CHOICES, blank=True, null=True)
    past_status_art_care = models.PositiveIntegerField(choices = ART_CARE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.patient_name.name_patient

    class Meta:
        verbose_name_plural = 'Status History'


class AnyIo(BaseContent):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name



PLHA_VISIT_STATUS_CHOICES = (
    (1,'Self'),
    (2,'Proxy'),
    (3,'Virtual')
)

YES_NO_CHOICES=(
    (1,'NO'),
    (2,'YES')
) 

VIRAL_REASON_CHOICES=(
    (1, 'General / Routine'),
    (2, 'Suspected Failuer'),
    (3, '2nd or 3rd Line Regimen Follow-up'),
    (4, 'Pregnant & Breastfeeding Women'),
    (5, 'Repeate Test after EAC')
)
P_N_CHOICES = (
    (1, 'Positive'),
    (2, 'Negative')
)

ADM_CHOICES = (
    (1, '4S Symptom positive & CD4<200 cells/mm3'),
    (2, '4S Negative & CD4 <200 cells/mm3'),
    (3, 'WHO Stage III/IV Disease')
)
WHO_CHOICES = (
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
    (4, 'IV')
)
SCREENING_STATUS =  (
    (1, '4S +ve'),
    (2, '4S -ve')
)
HBV_TESTRESULT_CHOICES = (
    (1, 'Positive'),
    (2, 'Negative'),
    (3, 'Awaiting Result')
)
CRAIG_INDICATION_CHOICE = (
    (1, 'Symptoms of Meningitis & CD4 <200'),
    (2, 'Asymptomatic & CD4 <200'),
    (3, 'WHO Stage III/IV')
)


class ARTVisit(BaseContent):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(ArtRegistration,on_delete=models.DO_NOTHING, related_name='patient_art_visit', null=True, blank=True)
    date_visit = models.DateField()
    plha_visit_status = models.PositiveIntegerField(choices = PLHA_VISIT_STATUS_CHOICES)
    pills_remaining = models.IntegerField(default=0)
    pills_prescribed_per_day = models.PositiveIntegerField(blank=True, null=True,default=0)
    pills_prescribed_last_visit = models.PositiveIntegerField(blank=True, null=True,default=0)
    cda_test_conducted = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    cda4_count =  models.IntegerField(blank=True, null=True, verbose_name = "CD4_count")
    viral_load_test_conducted = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    viral_load_reason = models.PositiveIntegerField(choices = VIRAL_REASON_CHOICES,blank=True, null=True)
    viral_load_count = models.BigIntegerField(blank=True, null=True)
    height = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=9)
    weight = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=9)
    systolic = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=9)
    diastolic = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=9)
    screening_conducted = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    night_sweats = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    s4_screening_status = models.PositiveIntegerField(choices = SCREENING_STATUS,blank=True, null=True)
    fever = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    cough = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    blood_test_conducted = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    blood_test_result_recieved = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    hemoglobin =  models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=9)
    fasting = models.IntegerField(blank=True, null=True)
    post_prandial = models.IntegerField(blank=True, null=True)
    random = models.IntegerField(blank=True, null=True)
    serum_creatinine = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=7)
    total_cholestrol  = models.IntegerField(blank=True, null=True)
    liver_test_conducted = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    liver_test_recieved = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    sbilirubin = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=7)
    sgot_ast = models.IntegerField(blank=True, null=True)
    sgpt_alt = models.IntegerField(blank=True, null=True)
    reactive_protein_conducted = models.PositiveIntegerField(choices = YES_NO_CHOICES, blank=True, null=True)
    reactive_protein = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=7)
    hbv_test_conducted = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    hcv_test_conducted = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    tb_lam_test_conducted = models.PositiveIntegerField(choices = YES_NO_CHOICES, blank=True, null=True)
    result_tb_lam_test = models.PositiveIntegerField(choices = HBV_TESTRESULT_CHOICES,blank=True, null=True)
    craig_test_conducted = models.PositiveIntegerField(choices = YES_NO_CHOICES, blank=True, null=True)
    result_craig = models.PositiveIntegerField(choices = HBV_TESTRESULT_CHOICES,blank=True, null=True)
    cryptococcal_menigitis_date = models.DateField(blank=True, null=True)
    cryptococcal_meningitis_place = models.CharField(max_length=250,blank=True, null=True)
    cryptococcal_meningitis_diagnosis = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    due_date_visit_artc = models.DateField(blank=True, null=True)
    any_oi_uuid = models.ManyToManyField(AnyIo, blank=True)
    syphilis_test_conducted = models.PositiveIntegerField(choices = YES_NO_CHOICES,blank=True, null=True)
    indication_lam = models.PositiveIntegerField(choices = ADM_CHOICES, blank=True, null=True)
    who_staging = models.PositiveIntegerField(choices = WHO_CHOICES,blank=True, null=True)
    pre_emptive_start_date = models.DateField(blank=True, null=True)
    pre_emptive_therapy_completion_date = models.DateField(blank=True, null=True)
    craig_indication  = models.PositiveIntegerField(choices = CRAIG_INDICATION_CHOICE, blank=True, null=True)
    adherance_percentage = models.IntegerField(blank=True, null=True)
    results_added = models.BooleanField(default=False)
    
    def __str__(self):
        return self.patient.name_patient
