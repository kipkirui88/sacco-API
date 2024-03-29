import requests

url = 'http://127.0.0.1:8000/api/members/3/create_savings/'  # Assuming 1 is the member's primary key
data = {
    "amount": 1.00
}

response = requests.post(url, json=data)

print(response.status_code)  # Check the response status code

try:
    print(response.json())  # Try to print the response content
except ValueError:
    print("Response content is not valid JSON")
