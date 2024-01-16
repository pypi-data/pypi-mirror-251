from celery import shared_task

from allianceauth.services.hooks import get_extension_logger

from esi.models import Token

from .provider import esi


logger = get_extension_logger(__name__)


@shared_task
def move_fleet_member(fleet_id: int, member_id: int, squad_id: int, wing_id: int, token_pk: int):
    token = Token.objects.get(pk=token_pk)

    esi.client.Fleets.put_fleets_fleet_id_members_member_id(
        fleet_id=fleet_id,
        member_id=member_id,
        movement={
            "squad_id": squad_id,
            "wing_id": wing_id,
            "role": "squad_member"
        },
        token=token.valid_access_token(),
    ).results()
