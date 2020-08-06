from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

# Import Model
from ..models.saving import Saving
# Import Serializer
from ..serializers import SavingSerializer, UserSerializer

class Savings(generics.ListCreateAPIView):
  permission_classes = (IsAuthenticated,)
  def get(self, request):
    """Index Request"""
    savings = Saving.objects.filter(owner=request.user.id)
    # display the savings to the end user
    data = SavingSerializer(savings, many=True).data
    return Response(data)

  serializer_class = SavingSerializer
  def post(self, request):
    """Create Request"""
    # Add user to request object
    request.data['saving']['owner'] = request.user.id
    # Serialize/Create Savings
    saving = SavingSerializer(data=request.data['saving'])
    # check if it exists (valid) and save it
    if saving.is_valid():
      s = saving.save()
      return Response(saving.data, status=status.HTTP_201_CREATED)
    else:
      return Response(saving.errors, status=status.HTTP_400_BAD_REQUEST)

class SavingDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (IsAuthenticated,)
  def get(self, request, pk):
    """Show Request"""
    # get specific saving account from pk (primary key)
    saving = get_object_or_404(Saving, pk=pk)
    data = SavingSerializer(saving).data

    if not request.user.id == data['owner']:
      raise PermissionDenied("Unauthorized, you do not have the right to view another's savings")

    return Response(data)

  def delete(self, request, pk):
    """Delete Request"""
    saving = get_object_or_404(Saving, pk=pk)

    if not request.user.id == saving.owner.id:
      raise PermissionDenied("Unauthorized, you do not have the right to delete another's savings")

    saving.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  def partial_update(self, request, pk):
    """Update Request"""
    # remove owner from request object
    if request.data['saving'].get('owner', False):
      del request.data['saving']['owner']

    saving = get_object_or_404(Saving, pk=pk)

    if not request.user.id == saving.owner.id:
      raise PermissionDenied("Unauthorized, you do not have the right to update another's savings")

    # Now we know its the right user
    request.data['saving']['owner'] = request.user.id

    ss = SavingSerializer(saving, data=request.data['saving'])

    if ss.is_valid():
      ss.save()
      print(ss)
      return Response(ss.data)
    return Response(ss.errors, status=status.HTTP_400_BAD_REQUEST)
