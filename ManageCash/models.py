from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField("auth.user", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"


class TransactionBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datetime = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class AddCash(TransactionBase):
    source = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.source} - {self.amount}"


class Expense(TransactionBase):

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
