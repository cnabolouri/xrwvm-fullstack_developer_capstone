# urls.py (inside djangoapp)

# Uncommented imports
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from . import views

app_name = "djangoapp"

urlpatterns = [
    # Home / dealerships list
    path("", views.get_dealerships, name="index"),
    path("dealers/", views.get_dealerships, name="dealers"),

    # Contact page (uses a template called contact.html)
    path("contact/", TemplateView.as_view(template_name="contact.html"), name="contact"),

    # Auth JSON endpoints
    path("register", views.registration, name="register"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("api/whoami", views.whoami, name="api-whoami"),

    # Dealer details + reviews
    path("dealer/<int:dealer_id>/", views.get_dealer_details, name="dealer_details"),
    # path("dealer/<int:dealer_id>/reviews/", views.get_dealer_reviews, name="dealer_reviews"),
    path(route='get_cars', view=views.get_cars, name ='getcars'),
    # Add a review (requires login in the view)
    # path("dealer/<int:dealer_id>/add-review/", views.add_review, name="add_review"),
    path("add_review", views.add_review, name="add_review"),

    path("get_dealers", views.get_dealerships, name="get_dealers"),
    path("get_dealers/<str:state>", views.get_dealerships, name="get_dealers_by_state"),
    path("dealer/<int:dealer_id>", views.get_dealer_details, name="get_dealer_details"),
    path("dealer/<int:dealer_id>/reviews", views.get_dealer_reviews, name="get_dealer_reviews"),
    path("reviews/dealer/<int:dealer_id>", views.get_dealer_reviews, name="get_dealer_reviews_alias"),

]

# Serve static & media in development
urlpatterns += static(settings.STATIC_URL, document_root=getattr(settings, "STATIC_ROOT", None))
urlpatterns += static(settings.MEDIA_URL, document_root=getattr(settings, "MEDIA_ROOT", None))
