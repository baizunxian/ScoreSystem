import django
django.setup()
from score.models import Student
from celery import shared_task


@shared_task
def delete_user(Sid):
    try:
        Student.objects.get(id=Sid).delete()
    except Exception as err:
        return err
    return 'SUCCESS'