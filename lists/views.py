from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.models import Item, List
from lists.forms import ItemForm

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "Empty list items aren't allowed"
        return render(request, 'home.html', {"error": error})
    return redirect(list_)


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:

            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "Empty list items aren't allowed"

    return render(request, 'list.html', {'list': list_, 'error': error})