from django.db import models

class Address(models.Model):
    """
    Django Model to store mailing addresses
    """
    apartment = models.CharField('Apartment', max_length=100, blank=True)
    street = models.TextField('Street', max_length=100)
    district = models.CharField('District', max_length=100)
    city = models.CharField('City', max_length=100)
    postal_code = models.CharField('Postal Code', max_length=100)
    state = models.CharField('State', max_length=100)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, to_field='code')
        
class Country(models.Model):
    name = models.CharField('Name', max_length=100)
    code = models.CharField('Country Code', max_length=2, unique=True, db_index=True)
    
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        
    def __str__(self):
        return self.code