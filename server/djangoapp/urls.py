from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for registration
    path(route='register', view=views.registration, name='register'),

    # path for login
    path(route='login', view=views.login_user, name='login'),

    # path for logout
    path(route='logout', view=views.logout_request, name='logout'),

    # Car makes / models for the review form
    path(route='get_cars', view=views.get_cars, name='getcars'),

    # Dealer listings, optionally filtered by state
    path(route='get_dealers', view=views.get_dealerships,
         name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships,
         name='get_dealers_by_state'),

    # Single dealer and its reviews
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details,
         name='dealer_details'),
    path(route='reviews/dealer/<int:dealer_id>',
         view=views.get_dealer_reviews, name='dealer_details_reviews'),

    # Add a review (login required)
    path(route='add_review', view=views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
