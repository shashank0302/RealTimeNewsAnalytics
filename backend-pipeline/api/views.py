# api/views.py
from django.http import JsonResponse

def test_endpoint(request):
    return JsonResponse({"message": "Hello, World!"})


