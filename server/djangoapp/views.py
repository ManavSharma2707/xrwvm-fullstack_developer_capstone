from datetime import datetime, timezone

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Terminate the user session; the empty userName tells the client that
    # nobody is logged in any more
    logout(request)
    return JsonResponse({"userName": ""})


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    # Refuse duplicate usernames
    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"userName": username, "error": "Already Registered"})

    # Create the user and log them in straight away
    user = User.objects.create_user(
        username=username, first_name=first_name, last_name=last_name,
        password=password, email=email)
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


# Return every car make / model pair (used by the review form dropdown)
def get_cars(request):
    # Seed the catalogue the first time it is requested
    if not CarMake.objects.exists():
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name}
            for car_model in car_models]
    return JsonResponse({"CarModels": cars})


# Return all dealerships, or only those in `state`
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    if dealerships is None:
        return JsonResponse(
            {"status": 502, "message": "Dealer service unavailable"})
    return JsonResponse({"status": 200, "dealers": dealerships})


# Return the reviews of a dealer, each tagged with its sentiment
def get_dealer_reviews(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})
    reviews = get_request("/fetchReviews/dealer/" + str(dealer_id))
    if reviews is None:
        return JsonResponse(
            {"status": 502, "message": "Review service unavailable"})
    for review_detail in reviews:
        response = analyze_review_sentiments(review_detail['review'])
        # Fall back to neutral if the sentiment service is unreachable
        review_detail['sentiment'] = (
            response['sentiment'] if response else "neutral")
    # Newest first: reviews carrying a timestamp sort by it, older seeded
    # reviews (no timestamp) follow, highest id first
    reviews.sort(
        key=lambda r: (r.get('time') or "", r.get('id', 0)), reverse=True)
    return JsonResponse({"status": 200, "reviews": reviews})


# Return the details of one dealer
def get_dealer_details(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})
    dealership = get_request("/fetchDealer/" + str(dealer_id))
    if dealership is None:
        return JsonResponse(
            {"status": 502, "message": "Dealer service unavailable"})
    return JsonResponse({"status": 200, "dealer": dealership})


# Submit a review for a dealer (logged-in users only)
@csrf_exempt
def add_review(request):
    if request.method != 'POST':
        return JsonResponse({"status": 405, "message": "POST required"})
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
    data = json.loads(request.body)
    # The author comes from the session, not from the client
    user = request.user
    data['user_id'] = user.id
    data['name'] = user.get_full_name() or user.username
    data['time'] = datetime.now(timezone.utc).isoformat()
    response = post_review(data)
    if response is None:
        return JsonResponse(
            {"status": 401, "message": "Error in posting review"})
    return JsonResponse({"status": 200, "review": response})
