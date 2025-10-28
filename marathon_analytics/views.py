# marathon_analytics/views.py
# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Result
import plotly
import plotly.graph_objs as go

class ResultsListView(ListView):
    '''View to display marathon results.'''

    model = Result
    template_name = 'marathon_analytics/results.html'
    context_object_name = 'results'
    paginate_by = 25 # how many records per page

    def get_queryset(self):
        '''limit the result queryset (for now).'''
        results = super().get_queryset()
        # return results[:25] # slice to only return first 25 records

        # look for URL paramaters to filter by:
        if 'city' in self.request.GET:
            city =  self.request.GET['city']

            if city:
                results = results.filter(city=city)
        
        return results

class ResultDetailView(DetailView):
    """Display results for a single runner"""

    model = Result
    template_name = 'marathon_analytics/result_detail.html'
    context_object_name = 'r'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = context['r']

        # Create a simple plotly chart showing split times
        first_half_seconds = (r.time_half1.hour * 60 + r.time_half1.minute) * 60 + r.time_half1.second
        second_half_seconds = (r.time_half2.hour * 60 + r.time_half2.minute) * 60 + r.time_half2.second
        
        x = ['first_half_seconds', 'second_half_seconds']
        y = [first_half_seconds, second_half_seconds]

        fig = go.Pie(labels=x, values=y)
        title_text = "Half Marathon Splits (seconds)"
        # Obtain the graph as an html div
        graph_div_splits = plotly.offline.plot({"data": [fig], 
                                                "layout_tile_text": title_text},
                                                output_type="div")

        context['graph_div_splits'] = graph_div_splits

        context['split_chart'] = plotly.io.to_html(fig, full_html=False)

        return context