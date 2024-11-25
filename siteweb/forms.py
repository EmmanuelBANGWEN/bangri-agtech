from django import forms
from django.forms.widgets import Textarea
from .models import Comment, Post, Subscriber

class CommentForm(forms.ModelForm):
    # username = forms.CharField(max_length=100, widget=TextInput(attrs={'class': 'form-control'}))
    # email = forms.EmailField( widget=TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': 3}))
    class Meta:
        model = Comment
        # fields = ['username', 'email', 'body'] 
        fields = ['body'] 

class SearchPost(forms.Form):
    query = forms.CharField(max_length=200)
    class Meta:
        fields = ['query']

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ('title', 'body', 'category') 


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']

class ConsultationForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nom")
    email = forms.EmailField(label="Adresse Email")
    consultation_type = forms.ChoiceField(
        choices=[
            ('Stratégies Agricoles', 'Stratégies Agricoles'),
            ('Choix Technologiques', 'Choix Technologiques'),
            ('Analyse de Performance', 'Analyse de Performance')
        ],
        label="Type de Consultation"
    )
    message = forms.CharField(widget=forms.Textarea, label="Message")

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nom")
    email = forms.EmailField(label="Adresse Email")
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea, label="Message")

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(max_length=500, widget=forms.Textarea)

from django import forms

class PostShareForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    to = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
