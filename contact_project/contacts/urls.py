from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_contacts, name='list_contacts'),
    path('add/', views.add_contact, name='add_contact'),
    path('edit/<int:contact_id>/', views.edit_contact, name='edit_contact'),
    path('delete/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('details/<int:contact_id>/', views.contact_details, name='contact_details'),
    path('export/', views.export_contacts, name='export_contacts'),
    path('import/', views.import_contacts, name='import_contacts'),
]
