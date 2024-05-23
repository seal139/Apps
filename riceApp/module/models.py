from django.db import models

# Create your models here.
class StockRecord(models.Model):
    dataType = models.BooleanField()
    year     = models.IntegerField()
    month    = models.IntegerField()
    avgStock = models.FloatField()

    def __str__(self):
        return f"{self.year}-{self.month} (Type: {'True' if self.type else 'False'}): {self.avgStock}"
    
class PopulationData(models.Model):
    year            = models.IntegerField()
    population      = models.FloatField()
    consumptionRate = models.FloatField()

    def __str__(self):
        return f"Year: {self.year}, Population: {self.population}, Consumption Rate: {self.consumptionRate}"
