from django.db.models.signals import pre_save
import threading
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


stash = threading.local()

def get_current_user():
    """Get the user whose session resulted in the current code running. (Only valid during requests.)"""
    return getattr(stash, 'current_user', None)

def set_current_user(user):
    stash.current_user = user

def onanymodel_presave(sender, **kwargs):
    current_user = get_current_user()
    if current_user is None or not current_user.is_authenticated:
        current_user = None

    obj = kwargs['instance']
    if hasattr(obj, 'modified_by_id'):
        if current_user and current_user.is_authenticated:
            obj.modified_by = current_user
    if not obj.pk:
        if hasattr(obj, 'created_by_id'):
            obj.created_by = current_user

pre_save.connect(onanymodel_presave)

class AutoCreatedAndModifiedFields(MiddlewareMixin):
    def process_request(self, request):
        set_current_user(request.user)
