from django import forms


class SquadDestinationForm(forms.Form):
    squad_destination = forms.ChoiceField(choices=(), required=True)

    def __init__(self, squads, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['squad_destination'].choices = squads
