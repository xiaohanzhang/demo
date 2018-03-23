from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeleteQuerySet, self).update(active=False)

    def hard_delete(self):
        return super(SoftDeleteQuerySet, self).delete()

    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.exclude(active=False)


class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.active_only = kwargs.pop('active_only', True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        qs = SoftDeleteQuerySet(self.model)
        if self.active_only:
            return qs.filter(active=True)
        return qs

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeleteModel(models.Model):
    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(active_only=False)

    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def delete(self):
        self.active = False
        self.save()

    def hard_delete(self):
        super(SoftDeleteModel, self).delete()

