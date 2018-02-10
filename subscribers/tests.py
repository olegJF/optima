from django.test import TestCase

from .models import Phone, Person, Region

class PersoneTestCase(TestCase):
    
    def setUp(self):
        self.ph1=Phone.objects.create(number="0111111111")
        self.ph2=Phone.objects.create(number="0222222222")
        self.ph3=Phone.objects.create(number="0333333333")
        self.rgn1=Region.objects.create(name="Киевская")
        self.rgn2=Region.objects.create(name="Одесская")
        self.rgn3=Region.objects.create(name="Харьковская")
        vova = Person(name="Вова", last_name='Маркин', email='vm@ua.fm', region=self.rgn1)
        vova.save()
        vova.phones.add(self.ph1.id,)
        serg = Person(name="Сергей", last_name='Тапкин', email='st@ua.fm', region=self.rgn2)
        serg.save()
        serg.phones.add(self.ph2.id, self.ph1.id)
        sveta = Person(name="Света", last_name='Анютина', email='sa@ua.fm', region=self.rgn2)
        sveta.save()
        sveta.phones.add(self.ph3.id, )
        georg = Person(name="Жора", last_name='Галкин', email='gg@ua.fm', region=self.rgn3)
        georg.save()
        georg.phones.add(self.ph1.id, self.ph3.id)


    def test_id_phones(self):
        first = Phone.objects.get(number="0111111111")
        second = Phone.objects.get(number="0222222222")
        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)

    def test_regions(self):
        first = Region.objects.get(name="Киевская")
        second = Region.objects.get(name="Одесская")
        self.assertEqual(first.name, "Киевская")
        self.assertEqual(second.name, "Одесская")

    def test_person_phones(self):
        user1 = Person.objects.get(email='vm@ua.fm')
        user2 = Person.objects.get(email='st@ua.fm')
        user3 = Person.objects.get(email='sa@ua.fm')
        user4 = Person.objects.get(email='gg@ua.fm')
        self.assertEqual(user1.phones.count(), 1)
        self.assertEqual(user1.phones.first().number, "0111111111")
        self.assertEqual(user2.phones.count(), 2)
        self.assertEqual(user3.phones.count(), 1)
        self.assertEqual(user3.phones.first().number, "0333333333")
        self.assertEqual(user4.phones.count(), 2)
        numbers =[]
        for i in user2.phones.all():
            numbers.append(i.number)
        self.assertIn("0111111111", numbers )
        self.assertIn("0222222222", numbers )

    def test_person_data(self):
        user1 = Person.objects.get(email='vm@ua.fm')
        user2 = Person.objects.get(last_name='Анютина')
        user3 = Person.objects.get(name="Сергей")
        user4 = Person.objects.get(name="Жора")
       
        self.assertEqual(user1.name, "Вова")
        self.assertEqual(user1.last_name, "Маркин")
        self.assertEqual(user2.name, "Света")
        self.assertEqual(user3.last_name, "Тапкин")
        self.assertEqual(user4.email, 'gg@ua.fm')

    def test_call_view_loads_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subscribers/home.html')
        self.assertEqual(1, response.context['page_number'])
    
    def test_add_phone_view(self):
        response = self.client.post('/new-number/', {'number': '0444444444'})
        ph4=Phone.objects.get(number='0444444444')
        self.assertEqual(ph4.number, '0444444444')

     
    def test_delete_user_view(self):
        user = Person.objects.get(email='vm@ua.fm')
        response = self.client.get('/delete/{id}/'.format(id=user.id))
        user_ = Person.objects.filter(id=user.id).first()
        self.assertEqual(user_, None)

    def test_get_absolute_url(self):
        user = Person.objects.get(email='st@ua.fm')
        path = '/detail/{id}/'.format(id=user.id)
        self.assertEqual(path, user.get_absolute_url())
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        
