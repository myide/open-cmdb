from .models import History


def create_history(name, user, instance, before, after, remark=''):
    History.objects.create(name=name, user=user, instance=instance, before=str(before), after=str(after), remark=remark)
