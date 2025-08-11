from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from pymongo import MongoClient
import os
# from dotenv import load_dotenv
# load_dotenv()
logger = logging.getLogger(__name__)


MONGODB_URI = os.getenv("MONGO_URI")
if not MONGODB_URI:
    raise ValueError("Missing MONGODB_URI in mongo_uri module")

client = MongoClient(MONGODB_URI)
db = client["pc_verification"]
collection = db["users"]

def verify_page(request):
    return render(request, 'verify.html')

@csrf_exempt
def verify_user(request):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "POST method required"}, status=405)
    
    try:
        data = json.loads(request.body)
        logger.info(f"Received data: {data}")
    except json.JSONDecodeError:
        logger.error("Invalid JSON")
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    username = data.get("username", "").strip()
    code = data.get("code", "").strip()

    if not username or not code:
        logger.error(f"Missing username or code. username: '{username}', code: '{code}'")
        return JsonResponse({"status": "error", "message": "Username and code are required"}, status=400)

    try:
        user = collection.find_one({"username": username, "code": code})
    except Exception as e:
        logger.error(f"Database error: {e}")
        return JsonResponse({"status": "error", "message": f"Database error: {e}"}, status=500)

    if user:
        return JsonResponse({
            "status": "success",
            "chat_id": user.get("chat_id"),
            "message": f"Your UID is {user.get('chat_id')}"
        })
    else:
        return JsonResponse({"status": "error", "message": "Invalid username or code"}, status=400)
