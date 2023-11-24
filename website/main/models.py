from django.db import models
from django.contrib.auth.models import User


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    book = models.ForeignKey('Books', on_delete=models.CASCADE, default=1)
    reservation_date = models.DateField(null=True, blank=True)
    deadline_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.reservation_date}'


class Books(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    synopsis = models.CharField(blank=True, null=True, max_length=200)
    reservations = models.ManyToManyField(Reservation, blank=True)
    reservas = models.IntegerField(default=0)
    data_lancamento = models.DateField()

    STATUS_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Reservado', 'Reservado'),
        ('Retirado', 'Retirado'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Disponível',
    )

    def __str__(self):
        return f'{self.name}, {self.author}'