from __future__ import annotations

from django.conf import settings
from django.db import models


class Problem(models.Model):
    title = models.CharField(max_length=100)
    question = models.TextField()
    correct_answer = models.TextField()
    case_sensitive = models.BooleanField(default=False)
    points = models.PositiveIntegerField()

    hunt = models.ForeignKey("Hunt", on_delete=models.CASCADE)
    solved_by = models.ManyToManyField("Team", blank=True)

    def __str__(self) -> str:
        return f"<{type(self).__name__}: {self.question[:20]}...>"

    def check_answer(self, answer: str, team: Team) -> bool:
        return (
            self.correct_answer == answer
            if self.case_sensitive
            else self.correct_answer.lower() == answer.lower()
        ) and not self.solved_by_team(team)

    def solved_by_team(self, team: Team) -> bool:
        return self.solved_by.filter(pk=team.pk).exists()


class Team(models.Model):
    name = models.CharField(max_length=100)
    points = models.PositiveIntegerField(default=0)

    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    hunt = models.ForeignKey("Hunt", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Hunt(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    end_time = models.DateTimeField()

    team_set: models.QuerySet[Team]
    problem_set: models.QuerySet[Problem]

    def __str__(self) -> str:
        return self.name
