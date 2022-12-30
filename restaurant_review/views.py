from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count
from django.urls import reverse
from django.utils import timezone

from restaurant_review.models import Restaurant, Review

# Create your views here.

def index(request):
    print('Request for index page received')

    restaurants = Restaurant.objects.annotate(avg_rating=Avg('review__rating')).annotate(review_count=Count('review'))

    # import pyvista as pv

    var_to_show = "_2"

    # sphere = pv.Sphere()
    # point, cell = sphere.ray_trace([0, 0, 0], [1, 0, 0], first_point=True)
    # var_to_show = f'Intersected at {point[0]:.3f} {point[1]:.3f} {point[2]:.3f}'

    # points, rays, cells = sphere.multi_ray_trace([[0, 0, 0]] * 3, [[1, 0, 0], [0, 1, 0], [0, 0, 1]], first_point=True)
    # string = ", ".join([f"({point[0]:.3f}, {point[1]:.3f}, {point[2]:.3f})" for point in points])
    # var_to_show = f'Rays intersected at {string}'

    return render(request, 'restaurant_review/index.html', {'restaurants': restaurants, 'var_to_show': var_to_show })


def details(request, id):
    print('Request for restaurant details page received')

    restaurant = get_object_or_404(Restaurant, pk=id)


    return render(request, 'restaurant_review/details.html', {'restaurant': restaurant})



def create_restaurant(request):
    print('Request for add restaurant page received')

    return render(request, 'restaurant_review/create_restaurant.html')


@csrf_exempt
def add_restaurant(request):
    try:
        name = request.POST['restaurant_name']
        street_address = request.POST['street_address']
        description = request.POST['description']
    except (KeyError):
        # Redisplay the question voting form.
        return render(request, 'restaurant_review/add_restaurant.html', {
            'error_message': "You must include a restaurant name, address, and description",
        })
    else:
        restaurant = Restaurant()
        restaurant.name = name
        restaurant.street_address = street_address
        restaurant.description = description
        Restaurant.save(restaurant)
                
        return HttpResponseRedirect(reverse('details', args=(restaurant.id,)))


@csrf_exempt
def add_review(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    try:
        user_name = request.POST['user_name']
        rating = request.POST['rating']
        review_text = request.POST['review_text']
    except (KeyError):
        #Redisplay the question voting form.
        return render(request, 'restaurant_review/add_review.html', {
            'error_message': "Error adding review",
        })
    else:
        review = Review()
        review.restaurant = restaurant
        review.review_date = timezone.now()
        review.user_name = user_name
        review.rating = rating
        review.review_text = review_text
        Review.save(review)
                
    return HttpResponseRedirect(reverse('details', args=(id,)))        