from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Prefetch
from django.db.models.functions import Coalesce

def index(request):
    user = request.user
    if user.is_authenticated:
        shorturls = (
            user.shorturls
            .annotate(
                latest_time=Coalesce('updated_at', 'created_at')
            )
            .prefetch_related('utms')
            .order_by('-latest_time')
        )
    return render(request, 'base.html', {
        'shorturls': shorturls,})
def create(request):
    pass