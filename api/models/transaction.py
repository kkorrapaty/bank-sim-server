from django.db import models
from django.contrib.postgres.fields import ArrayField

from .saving import Saving

class Transaction (models.Model):
  # fields
  # arrays for each
  deposit = ArrayField(models.DecimalField(max_digits=8, decimal_places=2, blank=True), blank=True)

  withdraw = ArrayField(models.DecimalField(max_digits=8, decimal_places=2, blank=True), blank=True)

  account = models.OneToOneField(
    Saving,
    on_delete=models.CASCADE,
    primary_key=True,
  )

  created_at = models.DateTimeField(auto_now_add=True)

  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    """Return string"""
    return f"Deposits: ${self.deposit} \nWithdraws: ${self.withdraw}"
