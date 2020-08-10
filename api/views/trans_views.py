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
from ..models.saving import Saving
# Import Serializer
from ..serializers import TransactionSerializer

class Transactions(generics.ListCreateAPIView):
  permission_classes = (IsAuthenticated,)
  def get(self, request):
    """Index Request"""
    # print('INSIDE', request.account)
    saving_account = Saving.objects.get(owner=request.user.id)

    transactions = Transaction.objects.filter(account=saving_account)
    # transactions = Transaction.objects.all()
    # display the transactions to the end user
    data = TransactionSerializer(transactions, many=True).data
    return Response(data)

  serializer_class = TransactionSerializer
  def post(self, request):
    """Create Request"""
    saving_account = Saving.objects.get(owner=request.user.id)
    # Add user to request object

    # request.data['transaction']['account'] = saving_account

    # Serialize/Create Transactions
    transaction = TransactionSerializer(data=request.data['transaction'])
    # check if it exists (valid) and save it
    if transaction.is_valid():
      # check account specified is in list of user's accounts
      # print('INSIDE', transaction.validated_data['account'].id)
      # print(saving_account.id)

      # account id
      id = transaction.validated_data['account'].id
      if not saving_account.id == id:
        # send custom error response -> not valid account
        raise PermissionDenied("Unauthorized, you do not have the right to create another's transactions")
      else:
        s = transaction.save()
        return Response(transaction.data, status=status.HTTP_201_CREATED)

      return Response(transaction.data)
      # dont need this
      # transaction.account = saving_account
      # Create transaction for assigned saving_account
      # saving_account.transaction_set.add(transaction)
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
