from django.db import models

class FarmerInput(models.Model):
    land_dimensions = models.CharField(max_length=100,null=True, blank=True)
    climate = models.CharField(max_length=100,null=True,blank=True)
    soil_type = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Input by farmer on {self.created_at}"


class Contact(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()
    desc = models.TextField()

    def __str__(self):
        return self.name + '-'+ self.email