from django import forms
from django.forms import ModelForm

from shop.models import Product, Category


class AddProductForm(ModelForm):
    class Meta:
        # Define the model and fields for the form
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price']

    def __init__(self, *args, **kwargs):
        # Initialize the form and set default widget classes
        super(AddProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            # Add Bootstrap 'form-control' class to visible fields
            visible.field.widget.attrs['class'] = 'form-control'


class AddCategoryForm(ModelForm):
    class Meta:
        # Define the model and fields for the form
        model = Category
        fields = ['title', 'sub_category', 'is_sub']
    
    def __init__(self, *args, **kwargs):
        # Initialize the form and set default widget classes
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        # Add specific classes to the category form fields
        self.fields['is_sub'].widget.attrs['class'] = 'form-check-input'
        self.fields['sub_category'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['class'] = 'form-control'


class EditProductForm(ModelForm):
    class Meta:
        # Define the model and fields for editing a product
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price']

    def __init__(self, *args, **kwargs):
        # Initialize the form and set default widget classes for editing
        super(EditProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            # Add Bootstrap 'form-control' class to visible fields
            visible.field.widget.attrs['class'] = 'form-control'
