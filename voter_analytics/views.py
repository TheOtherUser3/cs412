# File: views.py
# Author: Dawson Maska (dawsonwm@bu.edu), 10/28/2025
# Description: views file that calls on the html templates when called on 
# by urls.py and does any additional logic required to display the desired page

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm
from urllib.parse import urlencode
import plotly
import plotly.graph_objs as go



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
        voters = self.get_queryset()

        # Create a beautiful dictionary of dictionaries to only need one pass through the data
        dod = {'dobs': {}, 'parties': {}, 'elections': {'v20state': 0, 'v21town': 0, 'v21primary': 0, 'v22general': 0, 'v23town': 0}}

        for v in voters:
            if v.dob.year in dod['dobs']:
                dod['dobs'][v.dob.year] += 1
            else:
                dod['dobs'][v.dob.year] = 1
            if v.party in dod['parties']:
                dod['parties'][v.party] += 1
            else:
                dod['parties'][v.party] = 1
            for election in v.get_election_history():
                dod['elections'][election] += 1
            
        # Ensure that the pie chart doesn't break visually from all the little parties by combining them into 'Other'
        # But make sur that it isn't being filtered by a single tiny party first since we want to see that party then
        if len(dod['parties']) > 1:
            other = 0
            for party in list(dod['parties'].keys()):
                if party not in ['D ', "R ", 'U ']:
                    other += dod['parties'][party]
                    del dod['parties'][party]
            dod['parties']['Other'] = other
        # Now create the plots
        # DOB Histogram
        dob_fig = go.Bar(x=list(dod['dobs'].keys()), y=list(dod['dobs'].values()))
        dob_graph = plotly.offline.plot({"data": [dob_fig], 
                                            "layout": {
                                            "title": {"text": "Voter Birth Year Distribution", "x": 0.5}}},
                                            output_type="div")
        context['dob_graph'] = dob_graph


        # Party Pie Chart
        party_fig = go.Pie(labels=list(dod['parties'].keys()), values=list(dod['parties'].values()))
        party_graph = plotly.offline.plot({"data": [party_fig], 
                                            "layout": {
                                            "title": {"text": "Voter Political Party Distribution", "x": 0.5}}},
                                            output_type="div")
        context['party_graph'] = party_graph

        # Election Bar Chart
        election_fig = go.Bar(x=list(dod['elections'].keys()), y=list(dod['elections'].values()))
        election_graph = plotly.offline.plot({"data": [election_fig],
                                            "layout": {
                                            "title": {"text": "Voter Participation by Election", "x": 0.5}}},
                                            output_type="div")
        context['election_graph'] = election_graph

        return context
    
    def get_queryset(self):
        """Filter the queryset based on form input"""
        voters = super().get_queryset()
        form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            voters = filter_voters(voters, form)

        return voters