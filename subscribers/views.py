from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Person, Phone
from django.core.urlresolvers import reverse_lazy
from .forms import *


def home(request, page_number=1):
    all_persons = Person.objects.all()
    current_page = Paginator(all_persons, 10)
    try:
        item_list = current_page.page(page_number)
        contacts = {}
        for item in item_list:
            _phones = item.phones.all()
            
            for phone in _phones:
                _names = Person.objects.filter(phones=phone.id).exclude(id=item.id)
                
                if _names.exists():
                    print('ph',phone,_names)
                    contacts[item.id]=_names
                    
                    
                    
                    
                    
                    
    except InvalidPage:
        return redirect('/1/', page_number=1)

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

class PersonUpdate(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'subscribers/create.html'
    success_url = '/'

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