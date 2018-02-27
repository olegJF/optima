#from __future__ import unicode_literals

from unidecode import unidecode
from django.db import models
from django.conf import settings
from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=50, verbose_name = 'Область')
    

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'области'
        ordering = ['name']

    def __str__(self):
        return self.name




class Phone(models.Model):
    number = models.CharField(max_length=10, unique=True, )
   
    
    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
        ordering = ['number']

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
        
    
  

def send_email_to_new_user(sender, instance, created, *args, **kwargs):
    if created:
        subject = 'PhoneBook'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        txt_ = 'Поздравляю! Вы были добавленны в телефонную книгу!'
        
        sent_mail = send_mail(
                        subject,
                        txt_,
                        from_email,
                        recipient_list,
                        fail_silently=False)
        return sent_mail
    return False
# Для отправки писем расскоментировать строчку ниже.
# post_save.connect(send_email_to_new_user, sender=Person) 
