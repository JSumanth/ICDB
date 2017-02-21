"""
Views for the cars app.
"""
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.shortcuts import render_to_response
from cars.models import Car
from cars.forms import CarForm


def cars_view(request):
    """A view for cars."""
    if request.method == 'POST':
        # POST creates a car
        try:
            data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest('Not valid JSON!')

        form = CarForm(data)

        if form.is_valid():
            car = form.save()

            # Return a 201 CREATED response
            response = HttpResponse(status=201)
            response['Location'] = '/cars/' + str(car.id)

            return response
        else:
            return HttpResponseBadRequest('Invalid data!')
    elif request.method == 'GET':
        # GET returns a list of objects
        cars = Car.objects.all()
        return render_to_response('cars.json', {'cars': cars},
                                  mimetype='application/json')

    # Notify client of supported methods
    return HttpResponseNotAllowed(['GET', 'POST'])
