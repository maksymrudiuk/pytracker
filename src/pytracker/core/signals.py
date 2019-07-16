from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Task, Developer
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.fields.related import ForeignKey
from django.db.models.fields import SmallIntegerField
from .tasks import task_update_notification


@receiver(pre_save, sender=Task, dispatch_uid="task_update")
def task_update(sender, instance, **kwargs):

    changes = dict()
    old_values = dict()
    new_values = dict()

    try:
        old = sender.objects.get(pk=instance.pk)
        all_fields = instance._meta.get_fields(include_hidden=False)
        all_fields = [field for field in all_fields if not isinstance(field, ManyToOneRel)]
        for field in all_fields:
            if not getattr(old, field.name) == getattr(instance, field.name):
                if isinstance(field, ForeignKey):
                    old_values.update({field.name: getattr(old, field.name).user.email})
                    new_values.update({field.name: getattr(instance, field.name).user.email})
                elif isinstance(field, SmallIntegerField) and field.choices:
                    choice_dict = dict(field.choices)
                    old_values.update({field.name: choice_dict.get(getattr(old, field.name))})
                    new_values.update({field.name: choice_dict.get(getattr(instance, field.name))})
                else:
                    old_values.update({field.name: getattr(old, field.name)})
                    new_values.update({field.name: getattr(instance, field.name)})

        changes.update({'old': old_values})
        changes.update({'new': new_values})
        changes.update({'pk': instance.pk})
        task_update_notification.delay(changes, instance.creator.email)

    except instance.DoesNotExist:
        pass
