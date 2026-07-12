from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from game.models import Game
import string, random
import string, random

def public_join_view(request):
    if request.method == 'POST':
        game_code = request.POST.get('game_code', '').strip().upper()
        if Game.objects.filter(game_code=game_code).exists():
            return redirect('player_dashboard', game_code=game_code)
        else:
            return render(request, 'public_join.html', {'error': 'Invalid Game Session ID. Please check and try again.'})
    return render(request, 'public_join.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    if request.user.is_superuser:
        games = Game.objects.all().order_by('-id')
    else:
        games = Game.objects.filter(operator=request.user).order_by('-id')
    
    if request.method == 'POST':
        if 'create_game' in request.POST:
            game_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            game = Game.objects.create(game_code=game_code, operator=request.user)
            return redirect('operator_dashboard', game_code=game.game_code)
            
    return render(request, 'home.html', {'games': games})

@login_required
def delete_game_view(request, game_code):
    if request.method == 'POST':
        game = Game.objects.filter(game_code=game_code).first()
        if game and (request.user.is_superuser or game.operator == request.user):
            game.delete()
    return redirect('home')
