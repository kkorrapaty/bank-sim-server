from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

# import Model
from ..models.checking import Checking
# Import serializers
from ..serializers import CheckingSerializer, UserSerializer

class Checkings(generics.ListCreateAPIView):
  permission_classes = (IsAuthenticated,)
  def get(self, request):
    """Index Request"""
    checkings = Checking.objects.filter(owner=request.user.id)

    # display checkings to user
    data = CheckingSerializer(checkings, many=True).data
    return Response(data)

  serializer_class = CheckingSerializer
  def post(self, request):
    """Create Request"""
    # Add user to request object
    request.data['checking']['owner'] = request.user.id
    # Serialize/Create Checkings
    checking = CheckingSerializer(data=request.data['checking'])
    # check if it exists and save it
    if checking.is_valid():
      s = checking.save()
      return Response(checking.data, status=status.HTTP_201_CREATED)
    else:
      return Response(checking.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckingDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (IsAuthenticated,)
  def get(self, request, pk):
    """Show Request"""
    # get specific checking accoutn from pk
    checking = get_object_or_404(Checking, pk=pk)
    data = CheckingSerializer(checking).data

    if not request.user.id == data['owner']:
      raise PermissionDenied("Unauthorized, you do not have the right to view another's checkings")

    return Response(data)

  def delete(self, request, pk):
    """Delete Request"""
    checking = get_object_or_404(Checking, pk=pk)

    if not request.user.id == checking.owner.id:
      raise PermissionDenied("Unauthorized, you do not have the right to delete another's checkings")

    checking.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  def partial_update(self, request, pk):
    """Update Request"""
    # remove owner from request object
    if request.data['checking'].get('owner', False):
      del request.data['checking']['owner']

    checking = get_object_or_404(Checking, pk=pk)

    if not request.user.id == checking.owner.id:
      raise PermissionDenied("Unauthorized, you do not have the right update another's checkings")

    # we know its the right owner now
    request.data['checking']['owner'] = request.user.id

    cs = CheckingSerializer(checking, data=request.data['checking'])

    if cs.is_valid():
      cs.save()
      print(cs)
      return Response(cs.data)
    return Response(cs.errors, status=status.HTTP_400_BAD_REQUEST)
