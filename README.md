# EduHunt

A quick django application to create scavenger hunts.

> [!WARNING]
> I made this for my English class in ~1 hour, so
> it may be buggy, missing features, and very very hacky.


### Usage

Install ``uv``. Then:
```py
git clone https://github.com/JasonGrace2282/eduhunt scavhunt
cd scavhunt
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

You will also have to create an admin user in order to create
problems:
```py
uv run python manage.py createsuperuser
```
at which point you can head over to http://localhost:8000/admin to
create a hunt, teams, and questions.
