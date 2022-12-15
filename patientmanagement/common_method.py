#from AccessManagement.models import UserRoles
from datetime import datetime
from master_data.models import Boundary
from django.conf import settings 

def strip_uuid_space(uuid):
    uuid = str(uuid).strip(" ")
    return uuid

# def get_role_slug(login_user):
#     role_slug = ""
#     urroles = UserRoles.objects.get_or_none(user = login_user)
#     if urroles:
#         role_slug = urroles.role_type.slug
#     return role_slug

def dd_mm_yy_formate(date_formate):
    date_result = datetime.strptime(date_formate, "%d-%m-%Y").strftime('%Y-%m-%d')
    return datetime.strptime(date_result, '%Y-%m-%d')
    
def location_data_code(request):
    location_data_code = ""
    location_data_id = 0
    location = request.session.get('user_locations')
    if location:
        boundary_id = location[0]
        b = Boundary.objects.get(id=boundary_id)
        if b.code:
            location_data_code  = b.code
            location_data_id = b.id
    return location_data_code,location_data_id


# def generate_family_id(request,patients,patient_obj=None,snumber=None):
#     if not  snumber:
#         snumber = patients.count()+1
    
#     family_id = "FAM"+"-"+str(location_data_code(request))+"-"+str(snumber)
#     print(family_id)
#     if patient_obj:
#         if patients.filter(art_family_id=family_id).exclude(uuid=patient_obj.uuid).exists():
#             snumber = snumber+1
#             return generate_family_id(request,patients,patient_obj=patient_obj,snumber=snumber)
#     return family_id

# def get_number_from_family_id(family_code):   
#     if family_code:
#         family_code = str(family_code)
#         number = family_code.split('-')[-1]
#         if number.isdigit() :
#             number = int(number)
#         else:
#             number = 0
#     else:
#         number = 0
#     return number

# def generate_family_id(request,patients,patient_obj=None):
#     family_id_list = list(patients.exclude(uuid=patient_obj.uuid).values_list('art_family_id',flat=True))
#     if family_id_list:
#         max_num = max(map(get_number_from_family_id,family_id_list))+1
#     else:
#         max_num = 1
#     family_id = "FAM"+"-"+str(location_data_code(request))+"-"+str(max_num)
#     return family_id


def generate_family_id(request):
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))
    family_id = "FAM"+"-"+str(location_data_code(request)[0])+"-"+str(location_data_code(request)[1])+str(timestamp)
    return family_id

def validate_user_domain(user, locations, request):
    valid_domain = False
    role_code = user.role_type.slug
    art_boundary_domain = []
    request_domain = request.META['HTTP_HOST'].split('.')[0]

    if role_code in ['care-coordinator','counselor','lab-technician','smo','data-manager','staff-nurse']: # ART Center
        art_boundary_domain = Boundary.objects.filter(id__in = locations).values_list('slug',flat=True)
       
    elif role_code == 'lac-data-manager':
        #logic shoulod be based on the role and locattion configuration
        art_boundary_domain = Boundary.objects.filter(id__in = locations).values_list('parent__slug',flat=True)
    
    elif role_code in ['mdacs' ,'sacep-datamanager']:
        request_domain = request.META.get('HTTP_ORIGIN')
        art_boundary_domain = settings.PRIMARYBACKENDURL
       
    if request_domain in art_boundary_domain:
        valid_domain = True
        
    return valid_domain


# configure the subdomainame in site table

# from django.utils.text import slugify
# # expale https://mdacs-jobaid.in
# art_center = ["BYL Nair ART Center","KEM ART Center","LTMGH Sion ART Center","Pediatric Center of Excellence","Sir. J.J.ART Center","Sir. J.J.ART Center 2","BDBA ART Center","Dr R N Cooper ART Center","K B Bhabha (Bandra) ART Center","M T Agarwal ART Center","Rajawadi ART Center","Shatabdi Govandi ART Center","Siddharth ART Center","BJ Wadia Hospital","Godrej ART Center","K.J. Somaiya Medical College","L & T ART Center","GTB Hospital, Sewri","MBPT ART Center","Municipal STD Clinic, Mumbai"]
# b= Boundary.objects.filter(active=2, boundary_level__id = 3).update(slug=None)
# art_center_list = Boundary.objects.filter(active=2, boundary_level__id = 3,name__in=art_center)
# for art_center in art_center_list:
#     art_name = art_center.name
#     art_center_slug = slugify(art_name)
#     if Boundary.objects.filter(slug=art_center_slug).exists():
#         art_center_slug = art_center_slug + str(art_center.id)
#     if len(art_center_slug) >50:
#         art_center_slug = art_center_slug[:50]
#     art_center.slug = art_center_slug
#     art_center.save()
#     art_domain = art_center_slug + ".mdacs-jobaid.in"
#     # art_domain = art_center_slug + ".jobaidtest.com"
#     dispaly_name =  art_name[:43]+ " domain"
#     print('len of the name '+ str(len(dispaly_name)))
#     print(art_domain)
#     print(art_center.id)
#     print(dispaly_name)
#     print("====")
#     Site.objects.get_or_create(domain = art_domain, name = dispaly_name)