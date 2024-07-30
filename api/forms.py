from django import forms

USER_TYPE={
        ('', 'Choose user type'),
        ('admin', 'admin'),
        ('client', 'client'),
        ('freelancer', 'freelancer'),
    }

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})) 
    usertype = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={'class': 'form-control mb-3', 'placeholder': 'Choose user type'}))

class LoginForm(forms.Form): 
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email'})) 
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class NewProjectForm(forms.Form): 
    title = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'})) 
    description = forms.CharField( widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Title'})) 
    budget = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Title'})) 
    skills = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'})) 
    

class BiddingForm(forms.Form):
    bidAmount = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Title'}))
    estimatedTime = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Title'}))
    skills = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'})) 
    proposal = forms.CharField( widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Title'})) 

class ProjectSubmissionForm(forms.Form):
    projectLink = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'})) 
    manualLink = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'})) 
    submissionDescription = forms.CharField( widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Title'})) 
