from django.shortcuts import redirect, render

<<<<<<< HEAD
from lists.forms import ItemForm
=======
from lists.forms import ItemForm, ExistingListItemForm
>>>>>>> master
from lists.models import List

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
<<<<<<< HEAD
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
=======
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
>>>>>>> master
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})
