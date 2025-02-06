from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'email', 'address', 'company', 'notes']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        instance = self.instance

        if Contact.objects.filter(phone_number=phone_number).exclude(id=instance.id).exists():
            raise forms.ValidationError("A contact with this phone number already exists.")
        
        return phone_number
