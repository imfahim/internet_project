# forms.py

from django import forms

from internetProject.models import Complaint, Feedback


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


from django import forms


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'attachment', 'email', 'contact_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter Description'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Number'}),
        }


class Feedback(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'description', 'email']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter Description'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        }
