from django.db import models

# Create your models here.

class Guestbook(models.Model):
    name = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=20, default='')
    message = models.TextField(default=True)
    reg_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
         return 'Guestbook(%s, %s, %s, %s)' % (self.name, self.password, self.message, self.reg_date)