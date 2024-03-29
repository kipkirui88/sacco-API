import requests

# Replace the URL with your Django server address
base_url = 'http://localhost:8000/'

# Member ID for testing (replace with an existing member ID)
member_id = 3

# Withdrawal amount for testing
withdrawal_amount = 1000.0

# Endpoint for withdrawing from savings
withdrawal_url = base_url + f'api/members/{member_id}/withdraw_savings/'

# Data to send in the request
data = {
    'amount': withdrawal_amount,
}

response = requests.post(withdrawal_url, json=data)

if response.status_code == 200:
    print("Withdrawal from savings successful.")
    print("New savings balance:", response.json()['new_savings_balance'])
elif response.status_code == 400:
    print("Withdrawal from savings failed:")
    print("Message:", response.json()['message'])
else:
    print("Failed to withdraw from savings. Status code:", response.status_code)
