from .models import BloodCategory, Hospital
from accounts.models import AddState
def blood_category(request):
    blood_cat = BloodCategory.objects.all()
    hospitals = Hospital.objects.all()
    state_names = AddState.objects.all()
  
    return dict(blood_cat=blood_cat, hospitals=hospitals, state_names =state_names)