from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='parents')


    def __str__(self):
        return f'{self.name} => {self.parent}' if self.parent else f'{self.name}'
    

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
