from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CheckAnswer, ChooseHunt, ChooseTeam
from .models import Hunt


@login_required
def index(request):
    if request.method == "POST":
        form = ChooseHunt(request.POST)
        if form.is_valid():
            hunt = form.cleaned_data["hunt"]
            return redirect("dashboard:choose_team", hunt.id)
    else:
        form = ChooseHunt()
    return render(request, "dashboard/choose-hunt.html", {"form": form})


@login_required
def choose_team(request, hunt_id: int):
    hunt = get_object_or_404(Hunt.objects.filter(end_time__gt=timezone.now()), id=hunt_id)
    if hunt.team_set.filter(members=request.user).exists():
        return redirect("dashboard:hunt", hunt.id)
    if request.method == "POST":
        form = ChooseTeam(request.POST, hunt=hunt, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard:hunt", hunt.id)
    else:
        form = ChooseTeam(hunt=hunt, user=request.user)
    return render(request, "dashboard/choose-team.html", {"form": form, "hunt": hunt})


@login_required
def hunt_view(request, hunt_id: int):
    hunt = get_object_or_404(Hunt.objects.filter(end_time__gt=timezone.now()), id=hunt_id)
    team = get_object_or_404(hunt.team_set, members=request.user)

    if request.method == "POST":
        form = CheckAnswer(request.POST, hunt=hunt)
        if form.is_valid():
            if timezone.now() - request.user.last_attempt < timedelta(seconds=10):
                return JsonResponse({"result": "ratelimited"})
            request.user.last_attempt = timezone.now()
            request.user.save()
            points = form.compute_points(team)
            if points == 0:
                return JsonResponse({"result": "incorrect"})
            team.points = F("points") + points
            team.save(update_fields=["points"])
            return JsonResponse({"result": "success"})
        return JsonResponse(form.errors.as_json(), status=400)

    problems_solved = hunt.problem_set.filter(solved_by=team)
    problems = [(problem, problem in problems_solved) for problem in hunt.problem_set.all()]
    teams = hunt.team_set.all()
    return render(
        request,
        "dashboard/hunt.html",
        {
            "hunt": hunt,
            "problems": problems,
            "teams": teams,
            "user_team": team,
            "team_solved": hunt.problem_set.filter(solved_by=team),
        },
    )
