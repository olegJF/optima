from django.contrib import admin

from .models import *

# class PhoneInLine(admin.TabularInline):
#     model = Phone
#     extra = 1


class PersonAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Person
    
    #list_display = ('name','last_name','email', 'region', 'phones')

class PhoneAdmin(admin.ModelAdmin):
    # inlines = [
    #     PhoneInLine,
    # ]
    # 
    #exclude = ('only_for_one',)
    pass     
        
admin.site.register(Region)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Person, PersonAdmin)



    