from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from db_email.models import Email


@login_required(login_url='/admin/login/')
def html_message(request, email_id):
    if not request.user.is_staff:
        raise PermissionDenied()

    email = get_object_or_404(Email, pk=email_id)
    return HttpResponse(email.html, content_type='text/html')
