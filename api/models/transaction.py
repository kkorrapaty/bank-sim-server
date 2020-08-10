from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField

from .saving import Saving

class Transaction(models.Model):
  # fields

  # TRYING one Array of strings -> Cant update though so need to constantly save and send whole array
  # dep_with = ArrayField(models.CharField(max_length=10, blank=True), blank=True, default=list)

  # arrays for each
  # deposit = ArrayField(models.DecimalField(max_digits=8, decimal_places=2, blank=True), blank=True)
  #
  # withdraw = ArrayField(models.DecimalField(max_digits=8, decimal_places=2, blank=True), blank=True)

  # id = models.BigIntegerField(primary_key = True)

  # Not working:
  # dict_values = HStoreField(default=dict)

  change_in_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

  curr_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

  account = models.ForeignKey(
    Saving,
    on_delete=models.CASCADE,
  )

  created_at = models.DateTimeField(auto_now_add=True)

  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    """Return string"""
    return f"Deposits:"
    # ${self.deposit} \nWithdraws: ${self.withdraw}"
