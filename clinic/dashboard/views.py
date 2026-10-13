from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views import generic
from .models import Doctor, Visit, Patient, Treatment
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from .forms import SignUpForm, ReservationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required
def Reservation(req, pk=None):
    if pk:
        visit = get_object_or_404(Visit, pk=pk)
    else:
        visit = None

    if req.method != 'POST':
        form = ReservationForm(instance=visit)
        return render(req, 'dashboard/reservation.html', {'form':form, 'visit':visit})
    else:
        form = ReservationForm(req.POST, instance=visit)
        if form.is_valid():
            nuova_visita=form.save(commit=False)
            nuova_visita.save()
            return redirect('dashboard')
        else:
            return render(req, 'dashboard/reservation.html', {'form':form, 'visit':visit})

@login_required
def Reservation_delete(req, pk):
    visit=get_object_or_404(Visit, pk=pk)
    visit.delete()
    return redirect('dashboard')


def user_signup(request, next):
    if request.user.is_authenticated:
        return redirect('dashboard')            #porta alla dashbord se è loggato così non puoi rifare signup
    if request.method != 'POST':
        form = SignUpForm()
        return render(request, 'dashboard/signup.html', {'form': form})
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            auth_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            login(request, auth_user)
            Patient_group = Group.objects.get(name='Patients')
            auth_user.groups.add(Patient_group)
            Patient.objects.create(
                user=auth_user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                weight=form.cleaned_data['weight'],
                height=form.cleaned_data['height'],
                cf=form.cleaned_data['cf'],
                date_of_birth=form.cleaned_data['date_of_birth']

            )
            return HttpResponseRedirect(next)
        else:
            return render(request, 'dashboard/signup.html', {'form': form})

def dashboard(request):
    num_visits = request.session.get('num_visit', 0)
    num_visits = num_visits + 1
    request.session['num_visit'] = num_visits
    request.session.modified = True
    ctx = {
        'num_visit':num_visits,
    }
    return render(request, 'dashboard.html', context=ctx)

#DOCTOR
class DoctorListView(generic.ListView):
    model = Doctor
    paginate_by = 3

class DoctorDetailView(generic.DetailView):
    model = Doctor

#VISIT
class VisitListView(generic.ListView):
    login_url = '/accounts/login/'
    permission_required = 'dashboard.can_view_visit'
    model = Visit
    paginate_by = 3
    

class VisitDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    permission_required = 'dashboard.can_view_visit'
    model = Visit

#PATITIENT
class PatientListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    permission_required = 'dashboard.can_view_patient'
    model = Patient
    paginate_by = 3

class PatientDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    permission_required = 'dashboard.can_view_patient'
    model = Patient

#TREATMENT
class TreatmentListView(generic.ListView):
    model = Treatment
    paginate_by = 3

class TreatmentDetailView(generic.DetailView):
    model = Treatment
    
def esco(request):
    return render(request, 'esco.html')