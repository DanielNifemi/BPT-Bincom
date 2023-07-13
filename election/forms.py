from django import forms


class PollingUnitForm(forms.Form):
    polling_unit_name = forms.CharField(label='Polling Unit Name', max_length=255)
    location = forms.CharField(label='Location', max_length=255)
    party1 = forms.IntegerField(label='Party 1 Score')
    party2 = forms.IntegerField(label='Party 2 Score')
    party3 = forms.IntegerField(label='Party 3 Score')

    # Add more party fields as needed

    def clean(self):
        cleaned_data = super().clean()

        party1_score = cleaned_data.get('party1')
        party2_score = cleaned_data.get('party2')
        party3_score = cleaned_data.get('party3')
        # Add more party scores as needed

        if not all([party1_score, party2_score, party3_score]):
            raise forms.ValidationError('Please provide scores for all parties.')

        return cleaned_data


class PartyScoresForm(forms.Form):
    def __init__(self, *args, **kwargs):
        parties = kwargs.pop('parties')  # Retrieve the parties from the kwargs
        super(PartyScoresForm, self).__init__(*args, **kwargs)

        # Create dynamic form fields for each party
        for party in parties:
            self.fields[f'party_{party.id}'] = forms.IntegerField(label=party.name)

    def get_scores(self):
        scores = {}
        for field_name, field_value in self.cleaned_data.items():
            if field_name.startswith('party_'):
                party_id = int(field_name.split('_')[1])
                scores[party_id] = field_value
        return scores
