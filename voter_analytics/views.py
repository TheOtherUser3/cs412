# File: views.py
# Author: Dawson Maska (dawsonwm@bu.edu), 10/28/2025
# Description: views file that calls on the html templates when called on 
# by urls.py and does any additional logic required to display the desired page

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm
from urllib.parse import urlencode


#Helper function for filtering so I don't need to have that massive code section twice
def filter_voters(voters, form):
    min_dob = form.cleaned_data.get('min_dob')
    max_dob = form.cleaned_data.get('max_dob')
    voter_score = form.cleaned_data.get('voter_score')
    party = form.cleaned_data.get('party')
    v20state = form.cleaned_data.get('v20state')
    v21town = form.cleaned_data.get('v21town')
    v21primary = form.cleaned_data.get('v21primary')
    v22general = form.cleaned_data.get('v22general')
    v23town = form.cleaned_data.get('v23town')

    if min_dob:
        voters = voters.filter(dob__year__gte=min_dob)
    if max_dob:
        voters = voters.filter(dob__year__lte=max_dob)
    if voter_score:
        voters = voters.filter(voter_score=voter_score)
    if party:
        voters = voters.filter(party=party)
    if v20state:
        voters = voters.filter(v20state = v20state)
    if v21town:
        voters = voters.filter(v21town = v21town)
    if v21primary:
        voters = voters.filter(v21primary = v21primary)
    if v22general:
        voters = voters.filter(v22general = v22general)
    if v23town:
        voters = voters.filter(v23town = v23town)
    
    return voters

# Create your views here.

class VotersListView(ListView):
    """define a view to show all voters"""
    model = Voter
    template_name = 'voter_analytics/all_voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        """Add the form to the context data so we can render it in the template"""
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        # We need to stop the page parameter from polluting the entire URL with 100 different pages
        # Also need to send it back to the template so the pagination links can keep the other applied filters
        params = self.request.GET.copy()

        if 'page' in params:
            del params['page']

        context['querystring'] = urlencode(params)

        return context
    
    def get_queryset(self):
        """Filter the queryset based on form input"""
        voters = super().get_queryset()
        form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            voters = filter_voters(voters, form)

        return voters
    
class VoterDetailView(DetailView):
    """Define a view to show a single voter's details"""
    model = Voter
    template_name = 'voter_analytics/show_voter.html'
    context_object_name = 'voter'

class GraphsListView(ListView):
    """Define a view to show beautiful graphs of voter data"""
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        """Add the form to the context data so we can render it in the template"""
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)

        return context
    
    def get_queryset(self):
        """Filter the queryset based on form input"""
        voters = super().get_queryset()
        form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            voters = filter_voters(voters, form)

        return voters