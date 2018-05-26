from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Board(models.Model):
      subject = models.CharField(max_length=50, blank=True)
      name = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            null=False,
      )
      created_date = models.DateField(null=True, blank=True)
      memo = models.CharField(max_length=200, blank=True)
      hits = models.IntegerField(default = 0, blank=True)

      def __str__(self):
          return self.subject

class Comment(models.Model):
    cname = models.ForeignKey(
          settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE,
          null=False,
    )
    comm = models.CharField(max_length=50, blank=True)
    memo_id = models.ForeignKey(
        'Board',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comm
