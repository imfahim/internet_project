# forms.py

from django import forms

from internetProject.models import Complaint


class AccountDeletionRequestForm(forms.Form):
    email = forms.EmailField(label='Your email address')
    subject = forms.CharField(label='Subject Field', help_text='Please adhere to the format specified.')

    description = forms.CharField(
        label='Describe what you would like us to update/address',
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text='Be (i) specific, (ii) detailed, and (iii) concise.'
    )

    proof = forms.CharField(
        label='Provide proof/supporting evidence/documents',
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text='Provide proof (e.g., imgur, gyazo) that the request is authentic.'
    )

    attachments = forms.FileField(
        label='Attachments',
        help_text='Attach any relevant files if applicable',
        required=False
    )

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'attachment', 'email', 'contact_number']


