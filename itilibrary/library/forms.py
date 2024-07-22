from django import forms  
from .models import Book

class adddbook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("name", "author", "description", "price", "category", "photo", "is_active")