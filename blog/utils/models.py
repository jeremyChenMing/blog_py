import uuid
from django.db.models import *
from django.db import models


def gen_uuid():
    return uuid.uuid4().hex


def to_dict(self):
    opts = self._meta
    data = {}
    for f in opts.concrete_fields:
        if isinstance(f, models.ImageField):
            data[f.attname] = str(f.value_from_object(self))
        else:
            data[f.attname] = f.value_from_object(self)
    return data


class Model(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=gen_uuid, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.attname] = []
                else:
                    data[f.attname] = list(f.value_from_object(self).values_list('pk', flat=True))
            elif isinstance(f, ForeignKey) and f.value_from_object(self):
                data[f.name] = to_dict(getattr(self, f.name))
            else:
                data[f.attname] = f.value_from_object(self)
        return data



