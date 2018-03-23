from games.eveonline.models import EveCharacter
def get_main_eve_character(user):
    try:
        response = EveCharacter.objects.filter(user=user)[0].get_absolute()
    except:
        response = None

    return response

