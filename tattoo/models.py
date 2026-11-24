from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    class Role(models.TextChoices):
        undefined = 'undefined', 'Неопределенный'
        client = 'client', 'Клиент'
        master = 'master', 'Мастер'

    class Meta:
         verbose_name="Профиль"
         verbose_name_plural="Профили"

    user=models.OneToOneField("auth.User", on_delete=models.CASCADE)
    role = models.TextField("Роль", choices=Role, default=Role.undefined)

    def __str__(self):
         return self.user.username

@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, *args, **kwargs):
     if created:
          Profile.objects.create(user=instance)
        
class Service(models.Model):
    name = models.TextField("Название")
    price = models.IntegerField("Стоимость")
    duration = models.PositiveBigIntegerField("Длительность (мин)")
    image = models.ImageField("Картинка", null = True, upload_to="service")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
         return self.name

class Portfolio(models.Model):
    image = models.ImageField("Картинка", null = True, upload_to="portfolio")
    service = models.ForeignKey("tattoo.Service", on_delete=models.SET_NULL, null = True, blank = True)
    master = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null = True, blank = True)

    class Meta:
            verbose_name = "Портфолио"
            verbose_name_plural = "Портфолио"   

class Appointment(models.Model):
    class Status(models.TextChoices):
          confirmed = 'confirmed', 'Подтверждено'
          cancelled = 'cancelled', 'Отменено'
          completed = 'completed', 'Завершено'
    
    date = models.DateField("Дата")
    time = models.TimeField("Время")
    service = models.ForeignKey("tattoo.Service", on_delete=models.CASCADE, null = False, blank = True)
    master = models.ForeignKey("auth.User", on_delete=models.CASCADE, null = False, related_name="master_appointment", blank = True)
    client = models.ForeignKey("auth.User", on_delete=models.CASCADE, null = False, related_name="client_appointment", blank = True)
    comment = models.TextField("Комментарий", blank = True)

    class Meta:
                verbose_name = "Запись"
                verbose_name_plural = "Записи"

    def __str__(self):
         return f'{self.date} {self.time} {self.service}'

class Review(models.Model):
     class Rating(models.IntegerChoices):
           one = 1
           two = 2
           three = 3
           four = 4
           five = 5

     appointment = models.ForeignKey("tattoo.Appointment", on_delete=models.CASCADE, null = False, blank = True)
     rating = models.IntegerField("Оценка", choices = Rating, null = True)
     comment = models.TextField("Комментарий", blank = True)

     class Meta:
                 verbose_name = "Отзыв"
                 verbose_name_plural = "Отзывы"  