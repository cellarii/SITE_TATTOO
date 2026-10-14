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

"""
class Service(models.Model):
    title = models.TextField("Услуга")
    description = models.TextField("Описание")
    duration = models.TextField("Длительность")
    price = models.DecimalField("Цена")
    image = models.TextField("Изображение")

class Appointment(models.Model):
    data = models.DateField("Дата записи")
    time = models.TimeField("Время записи")
    client = models.ForeignKey()
    master = models.ForeignKey()
    comment = models.TextField("Комментарий")

class Portfolio(models.Model):
    master = models.ForeignKey()
    client = models.ForeignKey()
    image = models.TextField("Фотография")

class Studio(models.Model):
    city = models.TextField("Город")
    street = models.Model("Улица")
    building = models.Model("Дом")
"""