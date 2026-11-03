from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views import generic
from .models import Doctor, Visit, Patient, Treatment
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.db.models import Q
from .forms import SignUpForm, ReservationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

def _check_visit_owner(user, visit):
    """Un paziente può toccare solo le proprie visite.
    Dottori e segretari non hanno restrizioni."""
    if visit and hasattr(user, 'patient_profile') and visit.patient != user.patient_profile:
        raise PermissionDenied
@login_required
def Reservation(req, pk=None):
    if pk:
        visit = get_object_or_404(Visit, pk=pk)
        _check_visit_owner(req.user, visit)
    else:
        visit = None

    if req.method != 'POST':
        form = ReservationForm(instance=visit, user=req.user)
        return render(req, 'dashboard/reservation.html', {'form':form, 'visit':visit})
    else:
        form = ReservationForm(req.POST, instance=visit, user=req.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return render(req, 'dashboard/reservation.html', {'form':form, 'visit':visit})

@login_required
def Reservation_delete(req, pk):
    visit=get_object_or_404(Visit, pk=pk)
    _check_visit_owner(req.user, visit)
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

    def get_queryset(self):
        qs = Doctor.objects.all()
        q = self.request.GET.get('q', '').strip()
        if q:
            for term in q.split():
                qs = qs.filter(
                    Q(first_name__icontains=term) |
                    Q(last_name__icontains=term) |
                    Q(specialization__icontains=term)
                )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx

class DoctorDetailView(generic.DetailView):
    model = Doctor

#VISIT
class VisitListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    permission_required = 'dashboard.can_view_visit'
    model = Visit
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Doctors').exists():
            return Visit.objects.filter(doctor__user=user)      # doctor sees only his visits 
        return Visit.objects.all()                              # secretary sees every visit 
    

class VisitDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
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

    def get_queryset(self):
        qs = Treatment.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx

class TreatmentDetailView(generic.DetailView):
    model = Treatment
    
def esco(request):
    return render(request, 'esco.html')