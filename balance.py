import requests

url = 'http://127.0.0.1:8000/api/members/3/check_balance/'  # Assuming 1 is the member's primary key
response = requests.get(url)

print(response.status_code)  # Check the response status code

if response.status_code == 200:
    data = response.json()
    print("Member ID:", data['member_id'])
    print("Total Account Balance:", data['account_balance'])
else:
    print("Error:", response.text)  # Print the raw response content for debugging
