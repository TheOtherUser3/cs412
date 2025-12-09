# File: views.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/20/2025
# Description: views file that calls on the html templates when called on 
# by urls.py and does any additional logic required to display the desired page

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView, FormView
from .models import *
from .forms import *
from django.urls import reverse
from random import choice
from django.http import HttpResponse
from .engine.board_generator import generate_board
import json
from django.shortcuts import redirect
from .engine.run_match import run_match, simulate_matches
from .engine.plots import *
from plotly.offline import plot

class HomePageTemplateView(TemplateView):
    """Define a view class to display the home snake navigation page"""
    template_name = 'project/home_page.html'

####################################################################
# BOTS BOTS BOTS BOTS BOTS BOTS BOTS BOTS BOTS BOTS BOTS BOTS BOTS
####################################################################

class BotListView(ListView):
    """Define a view class to display the list of Bots"""
    model = Bot
    template_name = 'project/bots.html'
    context_object_name = 'bots'

    def get_queryset(self):
        return super().get_queryset().order_by('-timestamp')

class CreateBotView(CreateView):
    """Define a view class to display the create bot page"""
    template_name = 'project/create_bot.html'
    form_class = CreateBotForm

    def get_success_url(self):
        """Overide to redirect to bots list"""
        return reverse('bots')

class DeleteBotView(DeleteView):
    """Define a view class to delete a Bot"""
    model = Bot
    template_name = 'project/delete_bot.html'
    context_object_name = 'bot'

    def get_success_url(self):
        return reverse('bots')
    
class UpdateBotView(UpdateView):
    """Define a view class to update a Bot"""
    model = Bot
    template_name = 'project/update_bot.html'
    form_class = CreateBotForm

    def get_context_data(self, **kwargs):
        """Add additional context data of selected bot"""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        bot = Bot.objects.get(pk=pk)
        context['bot'] = bot 
        return context
    
    def get_success_url(self):
        """Overide to redirect to bots list"""
        return reverse('bots')
    
####################################################################
# BOARDS BOARDS BOARDS BOARDS BOARDS BOARDS BOARDS BOARDS BOARDS
####################################################################

class BoardListView(ListView):
    """Define a view class to display the list of Boards"""
    model = Board
    template_name = 'project/boards.html'
    context_object_name = 'boards'

    def get_queryset(self):
        return super().get_queryset().order_by('-timestamp')
    
class BoardDetailView(DetailView):
    """Define a view class to display the details of a Board"""
    model = Board
    template_name = 'project/board.html'
    context_object_name = 'board'

class CreateBoardView(CreateView):
    """Define a view class to display the create board page"""
    template_name = 'project/create_board.html'
    form_class = BoardGeneratorForm

    def post(self, request, *args, **kwargs):
        """When the form is submitted, generate the board and show preview,
        or save the board if confirmed, or regenerate if needed. This function + preview
        was *really* annoying to write."""
        action = request.POST.get('action')
        if action in ['confirm', 'regenerate']:
            # We already have the board data in hidden field, retrieve it.
            name = request.POST.get('name')
            width = int(request.POST.get('width'))
            height = int(width * 0.6) # 5:3 aspect ratio
            num_apples = int(request.POST.get('num_apples'))
            board_json = json.loads(request.POST.get("board_json_str"))
            wraparound = board_json.get('wrap', False)
            board_type = board_json.get('type', 'open')

            if action == 'confirm':
                # Save the board to the database
                board = Board(
                    name=name,
                    width=width,
                    height=height,
                    food_count=num_apples,
                    board_json=board_json,
                )
                board.save()
                return redirect('boards')
            else:
                # Regenerate the board
                board_data = generate_board(board_type, width, height, wraparound)
                 # Convert board data to JSON string for hidden field so we can convert it BACK to JSON later
                board_json_str = json.dumps(board_data)

                context = {
                    'name': name,
                    'board_type': board_type,
                    'width': width,
                    'height': height,
                    'num_apples': num_apples,
                    'board_json_str': board_json_str,
                    'board_json': board_data,
                }
                return render(request, 'project/board_preview.html', context)
        else:
            # Initial form submission. Generate board and show preview.
            form = self.get_form()
            if form.is_valid():
                name = form.cleaned_data['name']
                board_type = form.cleaned_data['board_type']
                width = int(form.cleaned_data['grid_width'])
                height = int(width * 0.6) # 5:3 aspect ratio
                num_apples = int(form.cleaned_data['num_apples'])
                wraparound = form.cleaned_data['wraparound']

                board_data = generate_board(board_type, width, height, wraparound)
                # Convert board data to JSON string for hidden field so we can convert it BACK to JSON later
                board_json_str = json.dumps(board_data)

                context = {
                    'name': name,
                    'board_type': board_type,
                    'width': width,
                    'height': height,
                    'num_apples': num_apples,
                    'board_json_str': board_json_str,
                    # NEED both, one for preview, one for hidden field for reconversion later
                    'board_json': board_data,
                }
                return render(request, 'project/board_preview.html', context)


class DeleteBoardView(DeleteView):
    """Define a view class to delete a Board"""
    model = Board
    template_name = 'project/delete_board.html'
    context_object_name = 'board'

    def get_success_url(self):
        return reverse('boards')
    
class UpdateBoardView(UpdateView):
    """Define a view class to update a Board"""
    model = Board
    template_name = 'project/update_board.html'
    form_class = BoardUpdateForm

    def get_context_data(self, **kwargs):
        """Add additional context data of selected board"""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        board = Board.objects.get(pk=pk)
        context['board'] = board 
        return context
    
####################################################################
# MATCHES MATCHES MATCHES MATCHES MATCHES MATCHES MATCHES MATCHES
####################################################################
    
class MatchListView(ListView):
    """Define a view class to display the list of Matches"""
    model = Match
    template_name = 'project/matches.html'
    context_object_name = 'matches'

    def get_queryset(self):
        return super().get_queryset().order_by('-started_at')
    
class MatchDetailView(DetailView):
    """Define a view class to display the details of a Match"""
    model = Match
    template_name = 'project/match.html'
    context_object_name = 'match'

# Apparently you can use FormView for regular forms wow!
class MatchCreateView(FormView):
    """Define a view class to display the create match page"""
    template_name = 'project/create_match.html'
    form_class = StartMatchForm

    def form_valid(self, form):
        """When the form is valid, start the match and redirect to match detail page"""
        bot1 = form.cleaned_data['bot1']
        bot2 = form.cleaned_data['bot2']
        board = form.cleaned_data['board']

        match = run_match(bot1, bot2, board)

        # Redirect to replay page
        return redirect('match_replay', pk=match.pk)

class MatchReplayView(DetailView):
    """Define a view class to display the match replay page"""
    model = Match
    template_name = 'project/match_replay.html'
    context_object_name = 'match'

class MatchDeleteView(DeleteView):
    """Define a view class to delete a Match"""
    model = Match
    template_name = 'project/delete_match.html'
    context_object_name = 'match'

    def get_success_url(self):
        return reverse('matches')
    
####################################################################
# LEADERBOARDS LEADERBOARDS LEADERBOARDS LEADERBOARDS LEADERBOARDS
####################################################################
class LeaderboardHubView(TemplateView):
    """Simple hub view to navigate the leaderboard pages"""
    template_name = "project/leaderboard_hub.html"

class GlobalLeaderboardView(ListView):
    template_name = "project/global_leaderboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = self.get_queryset()
        
        context["rows"] = rows
        return context
    
    def get_queryset(self):
        """Override the queryset to give us a list of rows for the stats of each bot"""
        # use select_related to avoid the N + 1 query problem 
        stats = BotBoardStats.objects.select_related("bot")
        totals = {}

        # Go through and accumulate each bot's total stats
        for s in stats:
            pk = s.bot.pk

            if pk not in totals:
                totals[pk] = {
                    "bot": s.bot,
                    "games": 0,
                    "wins": 0,
                    "losses": 0,
                    "draws": 0,
                    "avg_turns_sum": 0,
                    "avg_apples_sum": 0,
                    "entries": 0,
                }
            
            t = totals[pk]
            t["games"] += s.games
            t["wins"] += s.wins
            t["losses"] += s.losses
            t["draws"] += s.draws
            t["avg_turns_sum"] += s.avg_turns
            t["avg_apples_sum"] += s.avg_apples
            t["entries"] += 1

        # Make rows for our html template
        rows = []
        for pk in totals:
            t = totals[pk]
            rows.append({
                "bot": t["bot"],
                "games": t["games"],
                "wins": t["wins"],
                "losses": t["losses"],
                "draws": t["draws"],
                "avg_turns": t["avg_turns_sum"] / t["entries"],
                "avg_apples": t["avg_apples_sum"] / t["entries"],
                "win_rate": t["wins"] / t["games"] if t["games"] > 0 else 0
            })

        def sort_win_rate(row):
            return row['win_rate']

        #Sort by the win rate in decreasing order
        rows.sort(key=sort_win_rate, reverse=True)

        return rows


class BoardLeaderboardView(ListView):
    """Define a view to display leaderboard stats for a specific board
    (board pk passed in through url)"""
    model = BotBoardStats
    template_name = "project/board_leaderboard.html"
    context_object_name = "rows"

    def get_queryset(self):
        """Get rows for each bot of the board, and sort them by wins descending"""
        return BotBoardStats.objects.filter(
            board__pk=self.kwargs["pk"]
        ).order_by("-wins", "games") # Break ties, same wins with less games is more impressive
    
    def get_context_data(self, **kwargs):
        """Add additional context data of selected board"""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        board = Board.objects.get(pk=pk)
        context['board'] = board 
        return context
    
class BoardLeaderboardHubView(ListView):
    """Define a view for the board leadership hub where users select the 
    board they want to view leaderships records for"""
    model = Board
    template_name = "project/board_leaderboard_hub.html"
    context_object_name = "boards"

class SimulationView(FormView):
    """Define a view to simulate runs number of matches and show statistics
    in order to compare bots and boards more objectively"""
    template_name = "project/simulate.html"
    form_class = SimulationForm

    def form_valid(self, form):
        """Overrite form_valid to simulate matches, then graph the plots, 
        and send them to the next html template"""
        results = simulate_matches(
            bot1=form.cleaned_data["bot1"],
            bot2=form.cleaned_data["bot2"],
            board=form.cleaned_data["board"],
            num_runs=form.cleaned_data["runs"],
        )

        context = self.get_context_data(form=form)
        context["results"] = results

        #Call our plotting functions to get 4 html plots.
        context["plot_win_loss"] = plot(
            win_loss_plot(results),
            output_type="div",
            include_plotlyjs=False,
        )
        context["plot_win_rate"] = plot(
            win_rate_plot(results),
            output_type="div",
            include_plotlyjs=False,
        )
        context["plot_avg_turns"] = plot(
            avg_turns_plot(results),
            output_type="div",
            include_plotlyjs=False,
        )
        context["plot_avg_apples"] = plot(
            avg_apples_plot(results),
            output_type="div",
            include_plotlyjs=False,
        )

        return render(self.request, "project/simulation_results.html", context)
    




################################################################################
# enable the REST API for this application
from rest_framework import generics
from .serializers import *

class MoveEventListAPIView(generics.ListAPIView):
    """Exposes the API to return all MoveEvents for a given Match (for the JS replay)"""
    queryset = MoveEvent.objects.all()
    serializer_class = MoveEventSerializer
    pagination_class = None

    def get_queryset(self):
        """Override to filter by match_pk from URL"""
        match_pk = self.kwargs['match_pk']
        return MoveEvent.objects.filter(match__pk=match_pk).order_by('move_number')
