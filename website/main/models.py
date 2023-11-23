from django.db import models


class Books(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    synopsis = models.CharField(blank=True, null=True, max_length=200)
    reservas = models.IntegerField(default=0)
    data_lancamento = models.DateField()

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('unavailable', 'Unavailable'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
    )

    def __str__(self):
        return f'{self.name}, {self.author}'