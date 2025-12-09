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
from .engine.run_match import run_match

class HomePageTemplateView(TemplateView):
    """Define a view class to display the home snake navigation page"""
    template_name = 'project/home_page.html'

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
            author = request.POST.get('author')
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
                    author=author
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
                    'author': author
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
                author = form.cleaned_data['author']
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
                    'author': author
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
    


################################################################################
# enable the REST API for this application
from rest_framework import generics
from .serializers import *

class MoveEventListAPIView(generics.ListAPIView):
    """Exposes the API to return all MoveEvents for a given Match"""
    queryset = MoveEvent.objects.all()
    serializer_class = MoveEventSerializer
    pagination_class = None

    def get_queryset(self):
        """Override to filter by match_pk from URL"""
        match_pk = self.kwargs['match_pk']
        return MoveEvent.objects.filter(match__pk=match_pk).order_by('move_number')
