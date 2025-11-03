

# views.py

# --- Required imports (uncommented) ---
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime
import logging
import json
from django.views.decorators.http import require_http_methods
from .models import CarMake, CarModel
from .populate import initiate

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# TEMP STUBS so the views render without your cloud functions.
# Replace these with your actual helpers, e.g.:
# from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_review
# -----------------------------------------------------------------------------
def _stub_get_dealers_from_cf():
    # Minimal objects used by the templates. Replace with real data.
    return [
        {"id": 1, "full_name": "Seattle Auto Plaza", "city": "Seattle", "state": "WA"},
        {"id": 2, "full_name": "Portland Motors", "city": "Portland", "state": "OR"},
    ]

def _stub_get_dealer_by_id(dealer_id: int):
    for d in _stub_get_dealers_from_cf():
        if d["id"] == int(dealer_id):
            return d
    return None

def _stub_get_dealer_reviews_from_cf(dealer_id: int):
    return [
        {"name": "Sina", "review": "Great service!", "purchase": True, "purchase_date": "2024-08-12"},
        {"name": "Alex", "review": "Nice staff, quick process.", "purchase": False},
    ]

def _stub_post_review_to_cf(payload: dict):
    logger.info("Pretend posting to cloud function: %s", payload)
    return {"ok": True}
# -----------------------------------------------------------------------------


# ------------------------- AUTH JSON ENDPOINTS --------------------------------
@csrf_exempt
def login_user(request):
    """
    JSON login endpoint.
    Request: POST raw JSON: {"userName": "...", "password": "..."}
    Response: {"userName": "...", "status": "Authenticated"} or {"userName": "..."}
    """
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body or "{}")
        username = data.get("userName", "")
        password = data.get("password", "")
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)

    if not username or not password:
        return JsonResponse({"detail": "Missing credentials"}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"userName": username, "status": "Unauthorized"}, status=401)


# @csrf_exempt
# def logout_request(request):
#     """
#     JSON logout endpoint.
#     """
#     if request.method != "POST":
#         return JsonResponse({"detail": "Method not allowed"}, status=405)
#     logout(request)
#     return JsonResponse({"status": "Logged out"})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def logout_request(request):
    """
    Allow logging out via GET (for anchor links) or POST (for fetch/forms).
    - If it's an AJAX/JSON request, return JSON.
    - Otherwise redirect to homepage.
    """
    logout(request)

    wants_json = "application/json" in request.headers.get("Accept", "")
    if wants_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"status": "Logged out"})

    # Redirect after normal GET
    return redirect("djangoapp:index")


@csrf_exempt
def registration(request):
    """
    JSON registration endpoint.
    Request: POST raw JSON: {"userName": "...", "password": "...", "firstName": "...", "lastName": "..."}
    """
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)

    username = data.get("userName", "")
    password = data.get("password", "")
    first_name = data.get("firstName", "")
    last_name = data.get("lastName", "")

    if not username or not password:
        return JsonResponse({"detail": "Username and password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": "User already exists"}, status=409)

    user = User.objects.create_user(username=username, password=password,
                                    first_name=first_name, last_name=last_name)
    login(request, user)
    return JsonResponse({"userName": username, "status": "Registered"})



def whoami(request):
    if request.user.is_authenticated:
        return JsonResponse({"isAuthenticated": True, "userName": request.user.username})
    return JsonResponse({"isAuthenticated": False, "userName": ""})

# ----------------------------- PAGES ------------------------------------------
def get_dealerships(request):
    """
    Render the home page with a list of dealerships.
    Replace the stub with: dealers = get_dealers_from_cf()
    """
    dealers = _stub_get_dealers_from_cf()  # TODO: get_dealers_from_cf()
    context = {"dealership_list": dealers}
    return render(request, "Home.html", context)


def get_dealer_details(request, dealer_id: int):
    """
    Render dealer details page (dealer info + reviews).
    """
    dealer = _stub_get_dealer_by_id(dealer_id)  # TODO: real call
    if not dealer:
        messages.error(request, "Dealer not found.")
        return redirect("index")

    reviews = _stub_get_dealer_reviews_from_cf(dealer_id)  # TODO: real call
    context = {"dealer": dealer, "reviews": reviews}
    return render(request, "dealer_details.html", context)


def get_dealer_reviews(request, dealer_id: int):
    """
    If you keep a separate page just for reviews.
    """
    dealer = _stub_get_dealer_by_id(dealer_id)
    if not dealer:
        messages.error(request, "Dealer not found.")
        return redirect("index")

    reviews = _stub_get_dealer_reviews_from_cf(dealer_id)  # TODO
    context = {"dealer": dealer, "reviews": reviews}
    return render(request, "dealer_reviews.html", context)


@login_required(login_url="/login")
def add_review(request, dealer_id: int):
    """
    GET: render review form
    POST: submit review to backend (replace stub with your POST call)
    """
    dealer = _stub_get_dealer_by_id(dealer_id)
    if not dealer:
        messages.error(request, "Dealer not found.")
        return redirect("index")

    if request.method == "GET":
        return render(request, "add_review.html", {"dealer": dealer})

    # POST
    review_text = request.POST.get("review", "").strip()
    purchase = request.POST.get("purchase") == "on"
    purchase_date = request.POST.get("purchase_date") or None
    car_make = request.POST.get("car_make") or ""
    car_model = request.POST.get("car_model") or ""
    car_year = request.POST.get("car_year") or ""

    payload = {
        "time": datetime.utcnow().isoformat(),
        "name": request.user.get_full_name() or request.user.username,
        "dealership": dealer_id,
        "review": review_text,
        "purchase": purchase,
        "purchase_date": purchase_date,
        "car_make": car_make,
        "car_model": car_model,
        "car_year": car_year,
    }

    ok = _stub_post_review_to_cf(payload)  # TODO: replace with real post_review()
    if ok and (ok.get("ok") or ok is True):
        messages.success(request, "Thanks! Your review was submitted.")
    else:
        messages.error(request, "Could not submit review. Please try again.")

    return redirect("dealer_details", dealer_id=dealer_id)

def get_cars(request):
    # populate only if empty
    if CarMake.objects.count() == 0 or CarModel.objects.count() == 0:
        initiate()

    # If your FK is named 'make' (as above):
    qs = CarModel.objects.select_related("make").all()

    cars = [
        {"CarModel": c.name, "CarMake": c.make.name, "Type": c.type, "Year": c.year}
        for c in qs
    ]
    return JsonResponse({"CarModels": cars})

