from django.db import models
KZT = 'KZT'
USD = 'USD'
BTC = 'BTC'
EUR = 'EUR'
CURRENCYES = [
    (KZT, 'KZT'),
    (USD, 'USD'),
    (BTC, 'BTC'),
    (EUR, 'EUR')
]
class Post(models.Model):
    currency = models.CharField(max_length=5, choices=CURRENCYES, default=KZT)
    # currency = models.TextChoices('KZT', 'USD')

    def __str__(self):
        return f"{self.currency}"

