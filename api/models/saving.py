from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .user import User

# Savings Model -> One to One for now
class Saving(models.Model):
  # fields
  # minimum amount is $50
  amount = models.DecimalField(max_digits=8, decimal_places=2, validators = [MinValueValidator(50.00)])
  # connect to user
  # owner = models.ForeignKey(
  #   User,
  #   on_delete=models.CASCADE
  # )
  owner = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    primary_key=True,
  )

  created_at = models.DateTimeField(auto_now_add=True)

  updated_at = models.DateTimeField(auto_now=True)

  #return string
  def __str__(self):
    """Return String with info on amount in account"""
    if (self.amount < 50):
      return f"WARNING \nAmount: ${self.amount} -- Need at least $50"
    elif (self.amount == 50):
      return f"Amount: ${self.amount} -- Equal to Min Value"
    else:
      return f"Amount: ${self.amount}"

  def withdraw (self, ouput):
    """withdraw from account"""
    self.amount -= ouput
    return self.amount

  def deposit (self, input):
    """deposit into account"""
    self.amount += input
    return self.amount
