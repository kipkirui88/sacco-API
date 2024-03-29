import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import Member, Savings
from .serializers import MemberSerializer, SavingsSerializer
from decimal import Decimal
from django.db.models import Sum

# Function to send SMS
def send_sms(phone_number, message):
    username = 'koech'  # Replace with your Africastalking username
    api_key = '6fba7e43193b22b4a21fbd7227e8119f0b10dea1f9fd6dc26fe43770fb0'  # Replace with your Africastalking API key
    url = 'https://api.africastalking.com/version1/messaging'
    headers = {
        'ApiKey': api_key,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    data = {
        'username': username,
        'to': phone_number,
        'message': message
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        print('Message sent successfully!')
    else:
        print(f'Error sending message: {response.text}')

# View to withdraw from savings
class WithdrawSavingsView(APIView):
    def post(self, request, pk):
        try:
            member = Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return Response({"message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

        amount = Decimal(request.data.get('amount', 0))

        if amount <= 0:
            return Response({"message": "Withdrawal amount must be a positive value"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            savings = Savings.objects.filter(member=member).latest('id')
        except Savings.DoesNotExist:
            return Response({"message": "No savings account found for this member"}, status=status.HTTP_404_NOT_FOUND)
        except Savings.MultipleObjectsReturned:
            savings = Savings.objects.filter(member=member).order_by('-id').first()

        if savings.account_balance < amount:
            return Response({"message": "Insufficient savings balance"}, status=status.HTTP_400_BAD_REQUEST)

        new_savings_balance = savings.account_balance - amount
        savings.account_balance = new_savings_balance
        savings.save()

        # Calculate total account balance
        total_shares = member.account_balance
        total_savings = Savings.objects.filter(member=member).aggregate(total=Sum('account_balance'))['total']
        if total_savings is None:
            total_savings = 0
        total_balance = total_shares + total_savings

        # Send SMS after withdrawal
        message = f"Withdrawal of {amount} from savings successful. New savings balance: {new_savings_balance}, Total is {total_balance}. Regards, Koel Sacco"
        send_sms(member.phone_number, message)

        return Response({"message": "Withdrawal from savings successful", "new_savings_balance": str(new_savings_balance)}, status=status.HTTP_200_OK)

# View to check balance
class CheckBalanceView(APIView):
    def get(self, request, pk):
        try:
            member = Member.objects.get(pk=pk)

            # Calculate total account balance
            total_shares = member.account_balance
            total_savings = Savings.objects.filter(member=member).aggregate(total=Sum('account_balance'))['total']
            if total_savings is None:
                total_savings = 0
            total_balance = total_shares + total_savings

            # Send SMS with balance information
            message = f"Hello {member.full_name}, your savings is {total_savings}, Shares is {total_shares}, Total is {total_balance}. Regards, Koel Sacco"
            send_sms(member.phone_number, message)

            return Response({"member_id": member.id, "account_balance": str(total_balance)}, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response({"message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def retrieve_by_membership_number(self, request, membership_number):
        try:
            member = Member.objects.get(membership_number=membership_number)
            serializer = self.get_serializer(member)
            return Response(serializer.data)
        except Member.DoesNotExist:
            return Response({"message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def create_savings(self, request, pk=None):
        member = self.get_object()
        amount = Decimal(request.data.get('amount', 0))

        if amount <= 0:
            return Response({"message": "Amount must be a positive value"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the new savings account balance
        new_savings_balance = amount
        savings_data = {
            'member': member.id,
            'account_balance': new_savings_balance,
            'membership_number': member.membership_number
        }

        serializer = SavingsSerializer(data=savings_data)
        if serializer.is_valid():
            serializer.save()

            # Calculate total savings
            total_savings = Savings.objects.filter(member=member).aggregate(total=Sum('account_balance'))['total']
            if total_savings is None:
                total_savings = 0
            total_savings = total_savings + new_savings_balance

            # Calculate total shares (account_balance in Member model)
            total_shares = member.account_balance

            # Calculate total balance (sum of total savings and total shares)
            total_balance = total_savings + total_shares

            # Send SMS after savings creation
            message = f"Amount of {amount} saved successfully! New savings balance: {total_savings}, Total is {total_balance}. Regards, Koel Sacco"
            send_sms(member.phone_number, message)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)