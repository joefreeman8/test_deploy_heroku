from django.db import models

# Create your models here.
class Beer(models.Model):
    name = models.CharField(max_length=80, unique=True)
    style = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    abv = models.FloatField()
    brewery = models.ForeignKey(
        'breweries.Brewery',
        related_name='beers',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='beers',
        on_delete=models.CASCADE
    )
  
  
    def __str__(self):
        return f'{self.name} - {self.abv}%'