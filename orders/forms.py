from django import forms


class CatalogForm(forms.Form):
    discount = forms.BooleanField(
            label='Скидка',
            widget=forms.CheckboxInput,
            required=False)
    tax = forms.BooleanField(
            label='Налог',
            widget=forms.CheckboxInput,
            required=False)
    quantity = forms.IntegerField(
            label='Количество',
            widget=forms.NumberInput,
            min_value=0,
        )
