from django.shortcuts import render, redirect
from modules.eveonline.extensions.eveaudit.tasks import update_character_data
from django.contrib import messages

# Create your views here.
def update_eve_character(request, character):
    update_character_data.apply_async(args=[character])
    messages.add_message(request, messages.SUCCESS, 'Updated queued for character: %s. Come back in a little while.' % character)
    return redirect('eve-dashboard')
