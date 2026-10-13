from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('esco/', views.esco, name='esco'),
    path('doctors/', views.DoctorListView.as_view(), name='doctors'),
    path('visits/', views.VisitListView.as_view(), name='visits'),
    path('doctor/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('visit/<int:pk>/', views.VisitDetailView.as_view(), name='visit-detail'),
    path('patients/', views.PatientListView.as_view(), name='patients'),
    path('patient/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('signup/<path:next>/', views.user_signup, name='signup'),
    path('treatments/', views.TreatmentListView.as_view(), name='treatments'),
    path('treatment/<int:pk>/', views.TreatmentDetailView.as_view(), name='treatment-detail'),
    path('reservation/', views.Reservation, name='reservation'),
    path('reservation/<int:pk>/edit/', views.Reservation, name='reservation_update'),
    path('reservation/<int:pk>/delete/', views.Reservation_delete, name='reservation_delete')
]
    