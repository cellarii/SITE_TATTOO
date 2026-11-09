from io import BytesIO
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from tattoo.models import Service, Appointment, Portfolio, Review
from model_bakery import baker

# Create your tests here.
class ServiceViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_service(self):
        service = baker.make("tattoo.Service")

        r = self.client.get('/api/services/')
        data = r.json()
        print(data)

        assert service.name == data[0]['name']
        assert service.id == data[0]['id']
        assert service.price == data[0]['price']
        assert service.duration == data[0]['duration']
        assert len(data) == 1

    def test_create_service(self):
        r = self.client.post("/api/services/", {
            "name": "Японский стиль",
            "price": 40000,
            "duration": 240
        })

        new_service_id = r.json()['id']

        services = Service.objects.all()
        assert len(services) == 1

        new_service = Service.objects.filter(id = new_service_id).first()
        assert new_service.name == "Японский стиль"
        assert new_service.price == 40000
        assert new_service.duration == 240

    def test_delete_service(self):
        services = baker.make("Service", 10)
        r = self.client.get('/api/services/')
        data = r.json()
        assert len(data) == 10

        service_id_to_delete = services[3].id
        self.client.delete(f'/api/services/{service_id_to_delete}/')

        r = self.client.get('/api/services/')
        data = r.json()
        assert len(data) == 9

        assert service_id_to_delete not in [i['id'] for i in data]

    def test_update_service(self):
        services = baker.make("Service", 10)
        service: Service= services[2]

        r = self.client.get(f'/api/services/{service.id}/')
        data = r.json()
        assert data['name'] == service.name

        r = self.client.patch(f'/api/services/{service.id}/', {
            "name": "Новое имя"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/services/{service.id}/')
        data = r.json()
        assert data['name'] == "Новое имя"

        service.refresh_from_db()
        assert data['name'] == service.name

class AppointmentViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_appointment(self):
        service = baker.make("tattoo.Service")
        master = baker.make("auth.User")
        client = baker.make("auth.User")
        appointment = baker.make("tattoo.Appointment", service=service, master=master, client=client,)

        r = self.client.get('/api/appointments/')
        data = r.json()

        assert str(appointment.date) == data[0]['date']
        assert str(appointment.time) == data[0]['time']
        assert appointment.service.id == data[0]['service']
        assert appointment.master.id == data[0]['master']
        assert appointment.client.id == data[0]['client']
        assert appointment.comment == data[0]['comment']
        assert len(data) == 1

    def test_create_appointment(self):
        service = baker.make("tattoo.Service")
        master = baker.make("auth.User")
        client = baker.make("auth.User")

        r = self.client.post('/api/appointments/', {
            "date": "2026-11-11",
            "time": "10:00:00",
            "service": service.id,
            "master": master.id,
            "client": client.id
        })

        new_appointment_id = r.json()['id']

        appointments = Appointment.objects.all()
        assert len(appointments) == 1

        new_appointment = Appointment.objects.filter(id = new_appointment_id).first()
        assert str(new_appointment.date) == "2026-11-11"
        assert str(new_appointment.time) == "10:00:00"
        assert new_appointment.service == service
        assert new_appointment.master == master
        assert new_appointment.client == client

    def test_delete_appointment(self):
        service = baker.make("tattoo.Service")
        master = baker.make("auth.User")
        client = baker.make("auth.User")
        appointments = baker.make("tattoo.Appointment", service=service, master=master, client=client, _quantity = 10)
        
        r = self.client.get('/api/appointments/')
        data = r.json()
        assert len(data) == 10

        appointment_id_to_delete = appointments[3].id
        self.client.delete(f'/api/appointments/{appointment_id_to_delete}/')

        r = self.client.get('/api/appointments/')
        data = r.json()
        assert len(data) == 9

        assert appointment_id_to_delete not in [i['id'] for i in data]

    def test_update_appointment(self):
        service = baker.make("tattoo.Service")
        master = baker.make("auth.User")
        client = baker.make("auth.User")

        appointments = baker.make("tattoo.Appointment", service=service, master=master, client=client, _quantity=10,)
        appointment: Appointment = appointments[2]

        r = self.client.get(f'/api/appointments/{appointment.id}/')
        data = r.json()
        assert data['date'] == str(appointment.date)

        r = self.client.patch(f'/api/appointments/{appointment.id}/', {
            "date": "2006-11-11"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/appointments/{appointment.id}/')
        data = r.json()
        assert data['date'] == "2006-11-11"

        appointment.refresh_from_db()
        assert data['date'] == str(appointment.date)

class ReviewViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_review(self):
        service = baker.make("tattoo.Service")
        master = baker.make("auth.User")
        client = baker.make("auth.User")
        appointment = baker.make("tattoo.Appointment", service=service, master=master, client=client)
        review = baker.make("tattoo.Review", appointment = appointment)

        r = self.client.get('/api/reviews/')
        data = r.json()

        assert review.id == data[0]['id']
        assert review.appointment.id == data[0]['appointment']
        assert review.rating == data[0]['rating']
        assert review.comment == data[0]['comment']
        assert len(data) == 1

    def test_create_review(self):
        service = baker.make("tattoo.Service")
        master = baker.make("auth.User")
        client = baker.make("auth.User")
        appointment = baker.make("tattoo.Appointment", service=service, master=master, client=client)

        r = self.client.post('/api/reviews/', {
            "appointment": appointment.id,
            "rating": 5,
            "comment": "норм"
        })

        new_review_id = r.json()['id']

        reviews = Review.objects.all()
        assert len(reviews) == 1

        new_review = Review.objects.filter(id = new_review_id).first()
        assert new_review.appointment == appointment
        assert new_review.rating == 5
        assert new_review.comment == "норм"

    def test_delete_review(self):
        service = baker.make("tattoo.Service")
        master = baker.make("auth.User")
        client = baker.make("auth.User")
        appointment = baker.make("tattoo.Appointment", service=service, master=master, client=client)
        reviews = baker.make("tattoo.Review", appointment = appointment, _quantity = 10)
        
        r = self.client.get('/api/reviews/')
        data = r.json()
        assert len(data) == 10

        review_id_to_delete = reviews[3].id
        self.client.delete(f'/api/reviews/{review_id_to_delete}/')

        r = self.client.get('/api/reviews/')
        data = r.json()
        assert len(data) == 9

        assert review_id_to_delete not in [i['id'] for i in data]

    def test_update_reveiw(self):
        service = baker.make("tattoo.Service")
        master = baker.make("auth.User")
        client = baker.make("auth.User")
        appointment = baker.make("tattoo.Appointment", service=service, master=master, client=client)

        reviews = baker.make("tattoo.Review", appointment = appointment, _quantity = 10)
        review: Review = reviews[2]

        r = self.client.get(f'/api/reviews/{review.id}/')
        data = r.json()
        assert data['comment'] == str(review.comment)

        r = self.client.patch(f'/api/reviews/{review.id}/', {
            "comment": "крутокруто"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/reviews/{review.id}/')
        data = r.json()
        assert data['comment'] == "крутокруто"

        review.refresh_from_db()
        assert data['comment'] == review.comment

class PortfolioViewsetTestCase(TestCase):
    def setUp(self):
            self.client = APIClient()

    def test_get_portfolio(self):
        service = baker.make("tattoo.Service")
        master = baker.make("auth.User")
        portfolio = baker.make("tattoo.Portfolio", service = service, master = master, _create_files=True)

        r = self.client.get('/api/portfolios/')
        data = r.json()

        assert portfolio.id == data[0]['id']
        assert portfolio.service.id == data[0]['service']
        assert portfolio.master.id == data[0]['master']
        assert portfolio.image == data[0]['image']
        assert len(data) == 1

    def test_create_portfolio(self):
        service = baker.make("tattoo.Service")
        master = baker.make("auth.User")

        buf = BytesIO()
        Image.new('RGB', (1, 1)).save(buf, format='PNG')
        image_bytes = buf.getvalue()
        image = SimpleUploadedFile('test.png', image_bytes, content_type='image/png')

        r = self.client.post('/api/portfolios/', {
            "service": service.id,
            "master": master.id,
            "image": image,
        }, format='multipart')

        assert r.status_code == 201

        new_portfolio_id = r.json()['id']

        portfolios = Portfolio.objects.all()
        assert len(portfolios) == 1

        new_portfolio = Portfolio.objects.filter(id=new_portfolio_id).first()
        assert new_portfolio.service == service
        assert new_portfolio.master == master
        assert new_portfolio.image.read() == image_bytes

    def test_delete_portfolio(self):
        service = baker.make("tattoo.Service")
        master = baker.make("auth.User")
        portfolios = baker.make("tattoo.Portfolio", service = service, master = master, _create_files=True, _quantity = 10)

        r = self.client.get('/api/portfolios/')
        data = r.json()
        assert len(data) == 10

        portfolio_to_delete = portfolios[3].id
        self.client.delete(f'/api/portfolios/{portfolio_to_delete}/')

        r = self.client.get('/api/portfolios/')
        data = r.json()
        assert len(data) == 9

        assert portfolio_to_delete not in [i['id'] for i in data]

    def test_update_portfolio(self):
        service = baker.make("tattoo.Service")
        new_service = baker.make("tattoo.Service")
        master = baker.make("auth.User")
        portfolios = baker.make("tattoo.Portfolio", service=service, master=master, _create_files=True, _quantity=10)
        portfolio: Portfolio = portfolios[2]

        r = self.client.get(f'/api/portfolios/{portfolio.id}/')
        data = r.json()
        assert data['service'] == service.id

        r = self.client.patch(f'/api/portfolios/{portfolio.id}/', {
            "service": new_service.id
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/portfolios/{portfolio.id}/')
        data = r.json()
        assert data['service'] == new_service.id

        portfolio.refresh_from_db()
        assert data['service'] == portfolio.service.id