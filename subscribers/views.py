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
    # form = NewPhoneForm()
    sort = request.GET.get('sort', 'last_name')
    if sort not in SORT_LIST:
        sort = 'last_name'
    all_persons = Person.objects.all().order_by(sort)
    current_page = Paginator(all_persons, 10)
    try:
        item_list = current_page.page(page_number)
        # contacts = {}
        # for item in item_list:
        #     _phones = item.phones.all()
        #     
        #     for phone in _phones:
        #         _names = Person.objects.filter(phones=phone.id).exclude(id=item.id)
        #         
        #         if _names.exists():
        #             # print('ph',phone,_names)
        #             contacts[item.id] = _names
        #             
    except InvalidPage:
        return redirect('home', page_number=1)
    context = {
            # "form": form,
            'objects_list': item_list,
            'page_number': page_number
        }
    return render(request, 'subscribers/home.html', context)


class PersonDetail(DetailView):
    queryset = Person.objects.all()
    context_object_name = 'object'
    template_name = 'subscribers/detail.html'
    

def person_detail(request, pk):
    object = get_object_or_404(Person, id=pk)
    contacts = {}
    _phones = object.phones.all()
    _names_first_level = Person.objects.filter(phones__in=_phones).exclude(id=object.id)
    print(_names_first_level)
    if _names_first_level.exists():
        for name in _names_first_level:
            contacts[name] = Person.objects.filter(phones__in=name.phones.all()).exclude(id=object.id).distinct()            
    
    context = {
            'object': object,
            'contacts': contacts
        }
    return render(request, 'subscribers/detail.html', context)
    

class PersonCreate(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'subscribers/create.html'
    success_url = '/'
    

def add_person(request):
    context = {}
    if request.method == "POST":
        form = PersonForm1(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            last_name = data['last_name']
            email = data['email']
            region = data['region']
            phone = data['phone']
            phones = data['phones']
            print('phones', phones)
            ph = Phone.objects.filter(number=phone).first()
            person = Person(name=name, last_name=last_name, email=email, region=region)
            person.save()
            if ph is None:
                person.phones.create(number=phone)
            else:
                person.phones.add(ph.id)
            if len(phones)>0:
                for ph in phones:
                    person.phones.add(ph.id )
            # messages.success(request, '')
            return redirect('/')
        else:
            return render(request, 'subscribers/create.html', {"form": form})
    else:
        form = PersonForm1()
        context = {
            "form": form, 
            'action': 'Добавить нового пользователя.'
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
    context = {'object': person, 'form': form, 'action': 'Редактирование пользователя.'}
    if request.method == 'POST' and form.is_valid():
        form.save()
        # messages.success(request, 'Отредактировано!')
        return redirect('/')
    return render(request, 'subscribers/update.html', context)


class PersonDelete(DeleteView):
    model = Person
    success_url = '/'  # reverse_lazy('home')
    
    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
            
            
class NewPhoneCreate(CreateView):
    model = Phone
    form_class = NewPhoneForm
    template_name = 'subscribers/newnumber.html'
    success_url = '/add/'
