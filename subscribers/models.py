#from __future__ import unicode_literals

from unidecode import unidecode
from django.db import models
from django.core.validators import RegexValidator

from django.db.models.signals import m2m_changed
from django.dispatch import receiver


# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=50, verbose_name = 'Область')
    slug = models.CharField(max_length=50, verbose_name='Транслит', blank=True)

    class Meta():
        verbose_name = 'Область'
        verbose_name_plural = 'области'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = '{}'.format(unidecode(self.name))
        super(Region, self).save(*args, **kwargs)


class Phone(models.Model):
    number = models.CharField(max_length=10, unique=True, validators=[RegexValidator(r'^\d{1,10}$')])
    only_for_one = models.BooleanField(default=True, verbose_name='Используется только одним абонентом?')
    
    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'

    def __str__(self):
        return str(self.number)
        

class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(unique=True)
    region = models.ForeignKey(Region, verbose_name='Область', on_delete=models.CASCADE)
    phones = models.ManyToManyField(Phone, verbose_name='Телефон')
    
    class Meta:
        verbose_name = 'Абонент'
        verbose_name_plural = 'Абоненты'
        ordering = ['last_name']
        
    def __str__(self):
        return '%s %s' % (self.last_name, self.name)
        
    def get_absolute_url(self):
        return reverse('detail', kwargs={"pk": self.pk})
        
    # b =Person.objects.all().first()
    # p =  b.phones.all().first()
    # p.names.count() if >2 номер используется ещё кем то
  
  


        

