from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .user import User

# Checkings model -> Many to One
class Checking(models.Model):
  # fields
  amount = models.DecimalField(max_digits=8, decimal_places=2, validators = [MinValueValidator(50.00)])

  # Many checkings accounts per user
  owner = models.ForeignKey(
    User,
    on_delete=models.CASCADE
  )

  # TimeStamps
  created_at = models.DateTimeField(auto_now_add=True)

  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    """Return String with info"""
    return f"Amount: ${self.amount}"
