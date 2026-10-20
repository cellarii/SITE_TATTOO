from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.TextField("ФИО")
    group = models.ForeignKey("Group", on_delete = models.CASCADE, null = True)

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

class Group(models.Model):
    name = models.TextField("Название")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self) -> str:
        return self.name

        
class Service(models.Model):
    name = models.TextField("Название")
    price = models.IntegerField("Стоимость")
    duration = models.PositiveBigIntegerField("Длительность (мин)")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class Portfolio(models.Model):
    image = models.TextField()
    service = models.ForeignKey("tattoo.Service", on_delete=models.SET_NULL, null = True)
    master = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null = True)

    class Meta:
            verbose_name = "Портфолио"
            verbose_name_plural = "Портфолио"   

class Appointment(models.Model):
    class StatusChoices (models.TextChoices):
          CONFIRMED = 'confirmed', 'Подтверждено'
          CANCELLED = 'cancelled', 'Отменено'
          COMPLETED = 'completed', 'Завершено'
    
    date = models.DateField("Дата")
    time = models.TimeField("Время")
    service = models.ForeignKey("tattoo.Service", on_delete=models.CASCADE, null = False)
    master = models.ForeignKey("auth.User", on_delete=models.CASCADE, null = False, related_name="master_appointment")
    client = models.ForeignKey("auth.User", on_delete=models.CASCADE, null = False, related_name="client_appointment")
    comment = models.TextField("Комментарий")
    status = models.TextField("Статус", choices = StatusChoices.choices, default = StatusChoices.CONFIRMED) #ImageField, URLField

    class Meta:
                verbose_name = "Запись"
                verbose_name_plural = "Записи"  

class Review(models.Model):
     class RatingChoices(models.IntegerChoices):
           ONE = 1, "Ужасно"
           TWO = 2, "Плохо"
           THREE = 3, "Норм"
           FOUR = 4, "Хорошо"
           FIVE = 5, "Отлично"

     appointment = models.ForeignKey("tattoo.Appointment", on_delete=models.CASCADE, null = False)
     rating = models.IntegerField("Оценка", choices = RatingChoices.choices, null = True)
     comment = models.TextField("Комментарий")

     class Meta:
                 verbose_name = "Отзыв"
                 verbose_name_plural = "Отзывы"  