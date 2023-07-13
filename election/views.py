from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PollingUnitForm
from .models import PollingUnit, Result


def polling_unit_details(request, polling_unit_id):
    polling_unit = get_object_or_404(PollingUnit, id=polling_unit_id)
    results = polling_unit.announced_pu_results.all()  # Assuming you have a related_name specified for the
    # ForeignKey in AnnouncedPUResults model

    context = {
        'polling_unit': polling_unit,
        'results': results,
    }
    return render(request, 'polling_unit_details.html', context)


def local_government_list(request):
    # Retrieve all local governments
    local_governments = lga.objects.all()

    # Render the template with the retrieved data
    return render(request, 'local_government_list.html', {
        'local_governments': local_governments
    })


def get_polling_units_with_results(request):
    if request.method == 'POST':
        local_government_id = request.POST.get(
            'localGovernment')  # Retrieve the selected local government ID from the form submission
        polling_units = PollingUnit.objects.filter(local_government_id=local_government_id)

        # Retrieve the associated results for the polling units
        results = Result.objects.filter(polling_unit__local_government_id=local_government_id)

        context = {
            'polling_units': polling_units,
            'results': results
        }

        return render(request, 'polling_units.html', context)


def calculate_total_scores(request):
    # Perform the aggregation to calculate the total scores for each party
    total_scores = Result.objects.values('party').annotate(total_score=Sum('score'))

    context = {
        'total_scores': total_scores
    }

    return render(request, 'total_scores.html', context)


def create_polling_unit(request):
    if request.method == 'POST':
        polling_unit_form = PollingUnitForm(request.POST)
        party_scores_form = PartyScoresForm(request.POST)

        if polling_unit_form.is_valid() and party_scores_form.is_valid():
            polling_unit = polling_unit_form.save()  # Save the polling unit details to the PollingUnit table
            party_scores = party_scores_form.cleaned_data['party_scores']

            # Retrieve the generated unique ID for the new polling unit
            polling_unit_id = polling_unit.pk

            # Perform any additional processing or saving of party scores

            return redirect('polling_unit_detail', pk=polling_unit_id)  # Redirect to the polling unit detail page
    else:
        polling_unit_form = PollingUnitForm()
        party_scores_form = PartyScoresForm()

    return render(request, 'create_polling_unit.html', {
        'polling_unit_form': polling_unit_form,
        'party_scores_form': party_scores_form,
    })
