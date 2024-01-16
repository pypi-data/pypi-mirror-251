import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from allianceauth.services.hooks import get_extension_logger

from esi.decorators import token_required
from esi.models import Token

from .provider import esi
from .tasks import move_fleet_member
from .forms import SquadDestinationForm

logger = get_extension_logger(__name__)


@login_required
def index(request):
    return redirect('fleettools:fleetmoverlogin')


@login_required
@token_required(scopes=['esi-fleets.read_fleet.v1', 'esi-fleets.write_fleet.v1'])
def fleetmoverlogin(request, token: Token):
    return redirect('fleettools:fleetmover', token_pk=token.pk)


@login_required
def fleetmover(request, token_pk: int):
    token = get_object_or_404(Token, pk=token_pk)
    if token.user != request.user:
        return redirect('fleettools:fleetmoverlogin')

    if request.method == 'POST':
        wings = set()
        squads = set()

        if 'move-fleet' in request.POST and request.POST['move-fleet'] == 'on':
            move_fleet = True
        else:
            move_fleet = False
            wing_regex = re.compile(r'^wing-(?P<wing_id>\d+)$')
            squad_regex = re.compile(r'^squad-(?P<squad_id>\d+)$')

            for key, value in request.POST.items():
                if wing_regex.match(key) is not None and value == 'on':
                    wing_id = wing_regex.match(key).group('wing_id')
                    wings.add(int(wing_id))
                elif squad_regex.match(key) is not None and value == 'on':
                    squad_id = squad_regex.match(key).group('squad_id')
                    squads.add(int(squad_id))

        fleet_id = request.POST['fleet_id']

        fleet_members = (
            esi.client
            .Fleets
            .get_fleets_fleet_id_members(
                fleet_id=fleet_id,
                token=token.valid_access_token()
            )
            .results()
        )

        fleet_structure = (
            esi.client
            .Fleets
            .get_fleets_fleet_id_wings(
                fleet_id=fleet_id,
                token=token.valid_access_token()
            )
            .results()
        )

        destination_form = SquadDestinationForm(
            [
                (f"{wing['id']}-{squad['id']}", f"{wing['name']} -> {squad['name']}") for wing in fleet_structure for squad in wing['squads']
            ],
            request.POST,
        )

        if not destination_form.is_valid():
            messages.error(request, 'Invalid form data.')
            return redirect('fleettools:fleetmover', token_pk=token_pk)

        destination = destination_form.cleaned_data['squad_destination']

        wing_id, squad_id = destination.split('-')

        for member in fleet_members:
            if move_fleet or member['wing_id'] in wings or member['squad_id'] in squads:
                move_fleet_member.apply_async(
                    kwargs={
                        'fleet_id': fleet_id,
                        'member_id': member['character_id'],
                        'squad_id': int(squad_id),
                        'wing_id': int(wing_id),
                        'token_pk': token_pk,
                    },
                    priority=0,  # Highest priority
                )

        messages.success(request, 'Fleet updated successfully.')
        return redirect('fleettools:fleetmover', token_pk=token_pk)
    else:
        fleet_info = (
            esi.client
            .Fleets
            .get_characters_character_id_fleet(
                character_id=token.character_id,
                token=token.valid_access_token()
            )
            .results()
        )

        fleet_structure = (
            esi.client
            .Fleets
            .get_fleets_fleet_id_wings(
                fleet_id=fleet_info['fleet_id'],
                token=token.valid_access_token()
            )
            .results()
        )

        destination_form = SquadDestinationForm(
            squads=[
                (f"{wing['id']}-{squad['id']}", f"{wing['name']} -> {squad['name']}") for wing in fleet_structure for squad in wing['squads']
            ],
        )

    context = {
        'fleet': fleet_structure,
        'fleet_id': fleet_info['fleet_id'],
        'destination_form': destination_form,
    }

    return render(request, 'fleettools/fleetmover.html', context=context)
