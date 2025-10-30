# File: forms.py
# Author: Dawson Maska (dawsonwm@bu.edu), 10/29/2025
# Description: forms file that defines forms for voter_analytics application.

from django import forms
from datetime import date
from .models import Voter

class VoterFilterForm(forms.Form):
    """Define a form to filter voters based on criteria"""
    # Define some variables here to make things easier
    current_year = date.today().year
    YEAR_CHOICES = [(y, y) for y in range(1900, current_year + 1)]

    min_dob = forms.ChoiceField(
        choices=[('', 'Any')] + YEAR_CHOICES, required=False, label='Born After'
    )
    max_dob = forms.ChoiceField(
        choices=[('', 'Any')] + YEAR_CHOICES, required=False, label='Born Before'
    )
    voter_score = forms.ChoiceField(
        choices=[('', 'Any')] + [(x, str(x)) for x in range(6)], required=False, label='Voter Score'
    )
    party = forms.ChoiceField(
        choices=[('', 'Any')], required=False, label='Political Party'
    )
    v20state = forms.BooleanField(required=False, label='Voted in 2020 State Election')
    v21town = forms.BooleanField(required=False, label='Voted in 2021 Town Election')
    v21primary = forms.BooleanField(required=False, label='Voted in 2021 Primary Election')
    v22general = forms.BooleanField(required=False, label='Voted in 2022 General Election')
    v23town = forms.BooleanField(required=False, label='Voted in 2023 Town Election')

    def __init__(self, *args, **kwargs):
        """Apparently django loads the forms before the database unless we do this so we have to override init
        to make sure the party choices are loaded after the database is ready"""
        super().__init__(*args, **kwargs)
        # We can skip the list comprehension by just making it a list of tuples right here
        parties = Voter.objects.values_list('party', 'party').distinct()
        self.fields['party'].choices += list(parties)