from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Contact
from .forms import ContactForm
import csv
from django.http import HttpResponse

# List & Search Contacts
def list_contacts(request):
    query = request.GET.get('q', '')
    if query:
        contacts = Contact.objects.filter(name__icontains=query) | Contact.objects.filter(phone_number__icontains=query)
    else:
        contacts = Contact.objects.all()
    return render(request, 'contacts/list_contacts.html', {'contacts': contacts, 'query': query})

# Add a Contact
def add_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact added successfully!")
            return redirect('list_contacts')
    else:
        form = ContactForm()
    return render(request, 'contacts/add_contact.html', {'form': form})

# Edit a Contact
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact updated successfully!")
            return redirect('list_contacts')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/edit_contact.html', {'form': form, 'contact': contact})

# Delete a Contact
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == "POST":
        contact.delete()
        messages.success(request, "Contact deleted successfully!")
        return redirect('list_contacts')
    return render(request, 'contacts/delete_contact.html', {'contact': contact})

# Export Contacts to CSV
def export_contacts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone Number', 'Email', 'Address', 'Company', 'Notes'])

    contacts = Contact.objects.all()
    for contact in contacts:
        writer.writerow([contact.name, contact.phone_number, contact.email, contact.address, contact.company, contact.notes])

    return response

# Import Contacts from CSV
def import_contacts(request):
    if request.method == "POST" and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please upload a valid CSV file.")
            return redirect('import_contacts')

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)  # Skip header row

        for row in reader:
            Contact.objects.create(
                name=row[0],
                phone_number=row[1],
                email=row[2],
                address=row[3],
                company=row[4],
                notes=row[5]
            )

        messages.success(request, "Contacts imported successfully!")
        return redirect('list_contacts')

    return render(request, 'contacts/import_contacts.html')

# View for displaying a contact's details
def contact_details(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    return render(request, 'contacts/contact_details.html', {'contact': contact})

def list_contacts(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'name')  # Default sorting by name
    if query:
        contacts = Contact.objects.filter(name__icontains=query) | Contact.objects.filter(phone_number__icontains=query)
    else:
        if sort_by == 'name':
            contacts = Contact.objects.all().order_by('name')  # Sorting by name
        elif sort_by == 'created_at':
            contacts = Contact.objects.all().order_by('created_at')  # Sorting by creation date
        elif sort_by == 'updated_at':
            contacts = Contact.objects.all().order_by('updated_at')  # Sorting by last modified date
    return render(request, 'contacts/list_contacts.html', {'contacts': contacts, 'query': query})
