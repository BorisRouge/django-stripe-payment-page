from django import forms


class CatalogForm(forms.Form):
    discount = forms.BooleanField(label='Скидка', widget=forms.CheckboxInput)
    tax = forms.BooleanField(label='Налог', widget=forms.CheckboxInput)
    quantity = forms.IntegerField(label='Количество', widget=forms.NumberInput, min_value=0)