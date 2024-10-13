from django import forms
from django.utils import timezone

from .models import Hunt, Problem


class ChooseHunt(forms.Form):
    hunt = forms.ModelChoiceField(
        queryset=Hunt.objects.filter(end_time__gt=timezone.now()),
    )

class ChooseTeam(forms.Form):
    def __init__(self, *args, hunt: Hunt, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["team"] = forms.ModelChoiceField(
            queryset=hunt.team_set.all(),
        )
        self.user = user

    def save(self):
        team = self.cleaned_data["team"]
        team.members.add(self.user)
        team.save()


class CheckAnswer(forms.Form):
    answer = forms.CharField(max_length=255)

    def __init__(self, *args, hunt: Hunt, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["question"] = forms.ModelChoiceField(queryset=hunt.problem_set.all(), widget=forms.HiddenInput())

    def compute_points(self, team) -> int:
        question: Problem = self.cleaned_data["question"]
        answer = self.cleaned_data["answer"]
        if question.check_answer(answer, team):
            question.solved_by.add(team)
            question.save()
            return question.points
        return 0
