from django.shortcuts import render,redirect
from django.http import HttpResponse

from.models import *
from master_data.models import *
from django.views import View
# from .common_method import  get_role_slug, dd_mm_yy_formate, location_data_code,generate_family_id

from datetime import datetime


# Create your views here.
def plha_listing(request):
    artregistration=ArtRegistration.objects.all()

    return render(request,'plha/plha_listing.html',locals())


def plha_test(request):

    return render(request,'plha/test.html')


def index(request):

    return render(request,'index.html')

def patient_register(request):

    return render(request,'plha/patient registration.html')


def add_registration(request):
    artregister=ArtRegistration.objects().all()
    
    if request.method == 'POST':
        data = request.POST
        name_patient=data.get('name_patient')
        pre_art_no=data.get('pre_art_no')
        date_registration = data.get('date_registration')
        status_in_pre_art_care = data.get('status_in_pre_art_care')
        transferred_in = data.get('transferred_in')
        private_treatment_history = data.get('private_treatment_history')
        hiv_test_confirmed_date = data.get('hiv_test_confirmed_date')
        ictc_code = data.get('ictc_code')
        pid_number = data.get('pid_number')
        hiv_report = data.get('hiv_report')
        art_reg_diabetes = data.get('art_reg_diabetes')
        art_reg_hypertention = data.get('art_reg_hypertention')
        already_diagnosed_tb = data.get('already_diagnosed_tb')
        samvaad_application_id = data.get('samvaad_application_id')
        disclosure_with_family = data.get('disclosure_with_family')
        art_family_id = data.get('art_family_id')

        artregister=ArtRegistration.objects.create(name_patient=name_patient, pre_art_no=pre_art_no, date_registration=date_registration,
        status_in_pre_art_care=status_in_pre_art_care, transferred_in=transferred_in, private_treatment_history=private_treatment_history,
        hiv_test_confirmed_date=hiv_test_confirmed_date, ictc_code=ictc_code, pid_number=pid_number,hiv_report=hiv_report,art_reg_diabetes=art_reg_diabetes,
        art_reg_hypertention=art_reg_hypertention,already_diagnosed_tb=already_diagnosed_tb,samvaad_application_id=samvaad_application_id,disclosure_with_family=disclosure_with_family,
        art_family_id=art_family_id)
        artregister.save()
        return redirect('/')
    return render(request, 'plha/patient registration.html', locals())



        
        
class PatientRegistration(View):
    template_name = 'survey_forms/art_registration.html'

    def get(self, request):
        title = "Patient Registration"
        add = True
        art_status_choices = PRE_ART_STATUS_CHOICES
        art_cares_choices = ART_CARE_CHOICES
        hiv_reports = HIV_REPORT_CHOICES
        art_dia_hyps = ART_DIA_HYP
        # death_causes = CauseOfDeath.objects.filter(active=2).values("uuid","cause_name")
        states = Boundary.objects.filter(active=2, boundary_level__id = 1,operational=True).order_by('name').values('id',"name")
        return render(request,self.template_name,locals())
    
    def post(self, request):
        add = True
        art_status_choices = PRE_ART_STATUS_CHOICES
        art_cares_choices = ART_CARE_CHOICES
        hiv_reports = HIV_REPORT_CHOICES
        art_dia_hyps = ART_DIA_HYP
        # death_causes = CauseOfDeath.objects.filter(active=2).values("uuid","cause_name")
        states = Boundary.objects.filter(active=2, boundary_level__id = 1,operational=True).order_by('name').values('id',"name")
        login_user = request.user
        locations = request.session.get('user_locations',[])
        data = request.POST
        patient_name = data.get('patient_name')
        date_of_registration = data.get('date_of_registration')
        pre_art_no = data.get('pre_art_no')
        status_pre_art_care = data.get('status_pre_art_care')
        confirm_hiv_date = data.get('confirm_hiv_date')
        place_of_hiv = data.get('place_of_hiv')
        pid_num = data.get('pid_num')
        hiv_report = data.get('hiv_report')
        diagnosed_tb = data.get('diagnosed_tb')
        samvaad_id = data.get('samvaad_id')
        date_of_death = data.get('date_of_death')
        cause_of_death = data.get('cause_of_death')
        reason_death = data.get('reason_death')
        transferred_in_state = data.get('transferred_in_state')
        transferred_in_district = data.get('transferred_in_district')
        transferred_in_art = data.get('transferred_in_art')
        transferred_in = data.get('transferred_in')
        transferred_in_status = data.get('transferred_in_status')
        date_art_init = data.get('date_art_init')
        his_take_pvt_ngo = data.get('his_take_pvt_ngo')
        dt_of_pvt_ngo = data.get('dt_of_pvt_ngo')
        art_reg_no = data.get('art_reg_no')
        date_start_art = data.get('date_start_art')
        status_art_care = data.get('status_art_care')
        nikshay_id = data.get('nikshay_id')
        trans_out_conf_date = data.get('trans_out_conf_date')
        trans_artc_code = data.get('trans_artc_code')
        disclosure_with_family = data.get('disclosure_with_family')
        art_reg_diabetes = data.get('art_reg_diabetes')
        art_reg_hypertention = data.get('art_reg_hypertention')
        family_id = data.get('family_id')


        error = False
        if ArtRegistration.objects.filter(pid_number=pid_num, active = 2).exists():
            pid_exist = True
            error = True
        if nikshay_id:
            if ArtRegistration.objects.filter(nikshay_id=nikshay_id, active = 2).exists():
                error = True
                nikshay_exist = True
        if samvaad_id:
            if ArtRegistration.objects.filter(samvaad_application_id=samvaad_id, active = 2).exists():
                error = True
                samvaad_id_exist = True
        if locations:
            userart_center_patient = ARTPatientLinkage.objects.filter(art_center_id = locations[0], active=2).values_list('patient__uuid',flat=True)
            common_art_center_patients = ArtRegistration.objects.filter(uuid__in=userart_center_patient, active = 2)
            if pre_art_no:
                if common_art_center_patients.filter(pre_art_no=pre_art_no).exists():
                    error = True
                    pre_art_no_exist = True
            if art_reg_no:
                if common_art_center_patients.filter(art_reg_no=art_reg_no).exists():
                    error = True
                    art_reg_no_exist = True
        if not error:
            patient_registration = ArtRegistration.objects.create(
                name_patient = patient_name,
                # date_registration = dd_mm_yy_formate(date_of_registration),
                pre_art_no = pre_art_no,
                status_in_pre_art_care = status_pre_art_care,
                transferred_in = transferred_in,
                private_treatment_history = his_take_pvt_ngo,
                # hiv_test_confirmed_date = dd_mm_yy_formate(confirm_hiv_date),
                ictc_code = place_of_hiv,
                pid_number = pid_num,
                hiv_report = hiv_report,
                already_diagnosed_tb = diagnosed_tb,
                disclosure_with_family = disclosure_with_family,
                art_reg_diabetes = art_reg_diabetes,
                art_reg_hypertention = art_reg_hypertention,
                site_id_id             = request.session.get('site_id')
            )
            # Teack status ART Registractions Form
            statushistory_obj = StatusHistory.objects.create(
                patient_name = patient_registration,
                past_status_in_pre_art_care = status_pre_art_care,
                present_status_in_pre_art_care = status_pre_art_care,
                created_by = login_user)

            if status_art_care:
                statushistory_obj.past_status_art_care = status_art_care
                statushistory_obj.present_status_art_care = status_art_care

            statushistory_obj.save()

            # already_diagnosed_tb Tb line table record created if Yes
            # linking patient with art center 
            if locations:
                ARTPatientLinkage.objects.create(patient = patient_registration,
                art_center = Boundary.objects.get(id = locations[0], active=2),
                user = login_user,
                status = transferred_in
                )
                patient_registration.art_center_id = locations[0]
            patient_registration.save()

            if transferred_in_status:
                patient_registration.transfer_in_status = transferred_in_status
            if date_of_death:
                patient_registration.death_date = (date_of_death)
            if cause_of_death:
                patient_registration.death_cause_uuid = cause_of_death
            if samvaad_id:
                patient_registration.samvaad_application_id = samvaad_id
            if transferred_in_art:
                patient_registration.transferred_in_from_art_id=transferred_in_art
            if date_art_init:
                patient_registration.date_art_initiation = (date_art_init)
            if trans_out_conf_date:
                patient_registration.transfer_out_confirmation_data = (trans_out_conf_date)
            if nikshay_id:    
                patient_registration.nikshay_id = nikshay_id
            if status_art_care:
                patient_registration.art_care_status = status_art_care
            if dt_of_pvt_ngo:
                patient_registration.art_initiation_private_date = (dt_of_pvt_ngo)
            
            if family_id:    
                patient_registration.art_family_id = family_id
            else:
                # patients = ArtRegistration.objects.filter(active = 2)
                # family_id = generate_family_id(request)
                patient_registration.art_family_id =family_id

            if date_start_art:    
                patient_registration.art_start_date =(date_start_art)
            patient_registration.transferred_art_code = trans_artc_code
            patient_registration.death_reason = reason_death
            patient_registration.art_reg_no = art_reg_no
            added = True
            patient_registration.save()
        return render(request, self.template_name,locals() )





    
    
          