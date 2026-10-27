from django.test import TestCase
from rest_framework.test import APIClient
from tattoo.models import Service, Appointment, Portfolio, Review
from model_bakery import baker

# Create your tests here.
class ServiceViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
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