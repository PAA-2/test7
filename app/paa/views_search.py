from django.contrib.postgres.search import SearchQuery, SearchRank  # noqa: F401
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from .models import Action
from .helpers import can_view


@login_required
def search_view(request):
    q = (request.GET.get("q") or "").strip()
    results = []
    if q:
        if connection.vendor == "postgresql":
            query = SearchQuery(q, config="french")
            qs = Action.objects.extra(
                where=["search_vector @@ %s"],
                params=[query],
                select={"rank": "ts_rank(search_vector, %s)"},
                select_params=[query],
            ).order_by("-rank")[:200]
        else:
            qs = Action.objects.filter(title__icontains=q)[:200]
        results = [a for a in qs if can_view(a, request.user)]
    return render(request, "paa/search.html", {"q": q, "results": results})
