from django import forms
from lists.models import Item
<<<<<<< HEAD

EMPTY_ITEM_ERROR = "Empty list items aren't allowed"


class ItemForm(forms.models.ModelForm):
=======
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "Empty list items aren't allowed"
DUPLICATE_ITEM_ERROR = "You've already added this to your list!"


class ItemForm(forms.models.ModelForm):

>>>>>>> master
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

<<<<<<< HEAD
    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
=======

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list


    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)



    def save(self):
        return forms.models.ModelForm.save(self)
>>>>>>> master
