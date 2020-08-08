from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

# Import Model
from ..models.transaction import Transaction
# Import Serializer
from ..serializers import TransactionSerializer

class Transactions(generics.ListCreateAPIView):
  permission_classes = (IsAuthenticated,)
  def get(self, request):
    """Index Request"""
    # print('INSIDE', request.user.id)
    transactions = Transaction.objects.filter(account=request.user.id)
    # transactions = Transaction.objects.all()
    # display the transactions to the end user
    data = TransactionSerializer(transactions, many=True).data
    return Response(data)

  serializer_class = TransactionSerializer
  def post(self, request):
    """Create Request"""
    # Add user to request object
    request.data['transaction']['account'] = request.user.id
    # Serialize/Create Transactions
    transaction = TransactionSerializer(data=request.data['transaction'])
    # check if it exists (valid) and save it
    if transaction.is_valid():
      s = transaction.save()
      return Response(transaction.data, status=status.HTTP_201_CREATED)
    else:
      return Response(transaction.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (IsAuthenticated,)
  def get(self, request, pk):
    """Show Request"""
    # get specific transaction account from pk (primary key)
    transaction = get_object_or_404(Transaction, pk=pk)
    data = TransactionSerializer(transaction).data

    if not request.user.id == data['account']:
      raise PermissionDenied("Unauthorized, you do not have the right to view another's transactions")

    return Response(data)

  def delete(self, request, pk):
    """Delete Request"""
    transaction = get_object_or_404(Transaction, pk=pk)

    if not request.user.id == transaction.account.owner.id:
      raise PermissionDenied("Unauthorized, you do not have the right to delete another's transactions")

    transaction.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  def partial_update(self, request, pk):
    """Update Request"""
    # remove account from request object
    if request.data['transaction'].get('account', False):
      del request.data['transaction']['account']

    transaction = get_object_or_404(Transaction, pk=pk)

    if not request.user.id == transaction.account.owner.id:
      raise PermissionDenied("Unauthorized, you do not have the right to update another's transactions")

    # Now we know its the right user
    request.data['transaction']['account'] = request.user.id

    ss = TransactionSerializer(transaction, data=request.data['transaction'])

    if ss.is_valid():
      ss.save()
      print(ss)
      return Response(ss.data)
    return Response(ss.errors, status=status.HTTP_400_BAD_REQUEST)
