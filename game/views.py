from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Game, CalledNumber
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def broadcast_game_state(game_code, message_data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'game_{game_code}',
        {
            'type': 'game_message',
            'message': message_data
        }
    )

def player_dashboard(request, game_code):
    game = get_object_or_404(Game, game_code=game_code)
    called_numbers = game.called_numbers.all()
    context = {
        'game': game,
        'called_numbers': [cn.number for cn in called_numbers],
        'last_number': called_numbers.last().number if called_numbers.exists() else None,
    }
    return render(request, 'game/player_dashboard.html', context)

@login_required
def operator_dashboard(request, game_code):
    game = get_object_or_404(Game, game_code=game_code)
    if request.user != game.operator and request.user.role != 'admin':
        return redirect('home') # unauthorized

    called_numbers = game.called_numbers.all()
    context = {
        'game': game,
        'called_numbers': [cn.number for cn in called_numbers],
        'last_number': called_numbers.last().number if called_numbers.exists() else None,
    }
    return render(request, 'game/operator_dashboard.html', context)

@login_required
def call_next_number(request, game_code):
    if request.method == 'POST':
        game = get_object_or_404(Game, game_code=game_code)
        
        if game.status != 'Running':
            return JsonResponse({'error': 'Game is not running'}, status=400)

        called_numbers = game.called_numbers.values_list('number', flat=True)
        available_numbers = [n for n in range(1, 91) if n not in called_numbers]
        
        if not available_numbers:
            return JsonResponse({'error': 'All numbers called'}, status=400)
            
        next_number = random.choice(available_numbers)
        order = len(called_numbers) + 1
        
        CalledNumber.objects.create(
            game=game,
            number=next_number,
            order=order,
            called_by=request.user
        )
        
        # Broadcast via WebSockets
        broadcast_game_state(game_code, {
            'action': 'new_number',
            'number': next_number,
            'order': order,
            'operator': request.user.username
        })
        
        return JsonResponse({'success': True, 'number': next_number, 'order': order})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def change_game_status(request, game_code):
    if request.method == 'POST':
        game = get_object_or_404(Game, game_code=game_code)
        new_status = request.POST.get('status')
        if new_status in dict(Game.STATUS_CHOICES):
            game.status = new_status
            game.save()
            
            broadcast_game_state(game_code, {
                'action': 'status_change',
                'status': new_status
            })
            return JsonResponse({'success': True, 'status': new_status})
    return JsonResponse({'error': 'Invalid request'}, status=400)
