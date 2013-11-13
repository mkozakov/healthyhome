import urllib2  # Open URLs in python
import json     # Encode and Decode JSON

from django.views.generic import ListView
from django.shortcuts import redirect, render, get_object_or_404

from complaints.models import Building, Complaint
from complaints.forms import ComplaintForm

def report(request):
    # sticks in a POST or renders empty form
    form = ComplaintForm(request.POST or None)
    is_invalid = False

    if form.is_valid():
        location = lookup_location(form.cleaned_data)

        if location:
            complaint = form.save(commit=False)
            complaint.lat = location["results"][0]["geometry"]["location"]["lat"]
            complaint.long = location["results"][0]["geometry"]["location"]["lng"]
            complaint.save()
            return redirect('/building/1')
        else:
            is_invalid = True

    return render(request, 'complaints/submit.html', {'form': form, 'is_invalid': is_invalid})

def building(request, id):
    # sticks in a POST or renders empty form
    selected_building = Building.objects.get(id=id)
    complaints = Complaint.objects.filter(building_id=id)
    categories = {}
    for complaint in complaints:
        name = Complaint.CATEGORY_NAMES[complaint.category]
        if name in categories:
            categories[name] += 1
        else:
            categories[name] = 1 

    return render(request, 'complaints/building_page.html', {'categories' : categories, 'building' : selected_building})

def lookup_location(data):
    """
    Return the location of the address specified in data as a JSON object. If the address
    is invalid, return the empty string.
    @param data:
    @return:
    """
    address = '+'.join(str(data['address']).split())
    city = '+'.join(str(data['city']).split())
    province = '+'.join(str(data['province']).split())

    result = urllib2.urlopen(
        'http://maps.googleapis.com/maps/api/geocode/json?address=' +
        address + ',+' + city + ',+' + province + '&sensor=true')
    result = json.loads(result.read())

    if result['status'] == 'ZERO_RESULTS':
        result = ''
    return result
