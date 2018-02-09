from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, InvalidPage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Person, Phone
from django.core.urlresolvers import reverse_lazy
from .forms import *

SORT_LIST = ['last_name', '-last_name', 'name',
            '-name', 'email', '-email', 
            'region__name', 'region__name',
             'phones__number', 'phones__number']
             
def home(request, page_number=1):
    sort = request.GET.get('sort', 'last_name')
    if sort not in SORT_LIST: sort = 'last_name'
    all_persons = Person.objects.all().order_by(sort)
    current_page = Paginator(all_persons, 10)
    try:
        item_list = current_page.page(page_number)
        contacts = {}
        for item in item_list:
            _phones = item.phones.all()
            
            for phone in _phones:
                _names = Person.objects.filter(phones=phone.id).exclude(id=item.id)
                
                if _names.exists():
                    #print('ph',phone,_names)
                    contacts[item.id]=_names
                    
    except InvalidPage:
        return redirect('/1/', page_number=1)
    print(item_list)
    return render(request, 'subscribers/home.html', {'objects_list': item_list, 'contacts':contacts, 'page_number': page_number})
    
class PersonDetail(DetailView):
    queryset = Person.objects.all()
    context_object_name = 'object'
    template_name = 'subscribers/detail.html'
    

class PersonCreate(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'subscribers/create.html'
    success_url = '/'
    

def add_person(request):
    if request.method == "POST":
        form = PersonForm(request.POST or None)
        if form.is_valid():
            # instance = form.save(commit=False)
            form.save()
            # messages.success(request, '')
            return redirect('/')
        
    else:
        form = PersonForm()
        context = {
            "form": form, 
            'action':'Добавить нового пользователя.'
        }
    return render(request, 'subscribers/create.html', context)

class PersonUpdate(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'subscribers/create.html'
    success_url = '/'
    
def edit_person(request, pk):
    person = get_object_or_404(Person, id=pk)
    form = PersonForm(request.POST or None, instance=person)
    context = {'object': person, 'form': form, 'action':'Редактирование пользователя.'}
    if request.method == 'POST' and form.is_valid():
        form.save()
        # messages.success(request, 'Отредактировано!')
        return redirect('/')
    return render(request, 'subscribers/update.html', context)

class PersonDelete(DeleteView):
    model = Person
    success_url = '/' #reverse_lazy('home')
    
    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
            
            
class NewPhoneCreate(CreateView):
    model = Phone
    form_class = NewPhoneForm
    template_name = 'subscribers/newnumber.html'
    success_url = '/add/'