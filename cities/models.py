from django.db import models
from django.urls import reverse


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Город')

    def __str__(self):
        return self.name

    # после добавления записи в эту таблицу с помощью класса форм сформированной для этой таблицы и генерика createview
    # эта функция делает редирект на страницу с записью после ее добавления
    def get_absolute_url(self):
        return reverse('cities:detail', kwargs={'pk': self.pk})


    class Meta:
        # Русификация
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        # Сортирвоака при отображении
        ordering = ['name']
