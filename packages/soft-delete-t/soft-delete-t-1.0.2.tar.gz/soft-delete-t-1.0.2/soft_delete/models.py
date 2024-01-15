from django.db import models, transaction
from django.db.models.deletion import get_candidate_relations_to_delete
from django.utils import timezone

try:
    from rest_framework.exceptions import ValidationError
except ModuleNotFoundError:
    from django.core.exceptions import ValidationError


class SoftDeleteQuerySet(models.query.QuerySet):

    def hard_delete(self):
        return super().delete()


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, self._db).filter(is_deleted=-1)


class DeletedQuerySet(models.query.QuerySet):
    def restore(self, *args, **kwargs):
        qs = self.filter(*args, **kwargs)
        for obj in qs:
            obj.restore(cascade=True)


class DeletedManager(models.Manager):
    def get_queryset(self):
        return DeletedQuerySet(self.model, self._db).exclude(is_deleted=-1)


class GlobalManager(models.Manager):
    pass


def process_relates(related, instance, related_queryset):
    field = related.field
    related_model = related.related_model
    if field.remote_field.on_delete == models.CASCADE:
        return related_queryset(related_model, field, instance)
    if field.remote_field.on_delete == models.PROTECT:
        raise ValidationError(f'有关联的{related_model.__name__}数据不能删除')
    return []


def restore_process_relates(related, instance, related_queryset):
    field = related.field
    related_model = related.related_model
    if field.remote_field.on_delete == models.CASCADE:
        return related_queryset(related_model, field, instance)
    return []


class SoftDeleteModel(models.Model):
    is_deleted = models.IntegerField('是否删除', default=-1)
    deleted_at = models.DateTimeField('删除时间', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    cascade = models.BooleanField('是否是级联删除', default=False)
    objects = SoftDeleteManager()
    deleted_objects = DeletedManager()
    global_objects = GlobalManager()

    class Meta:
        abstract = True

    @transaction.atomic
    def delete(self, cascade=False, *args, **kwargs):
        self._meta.auto_created = True
        self._state.adding = False
        models.signals.pre_delete.send(sender=self.__class__, instance=self)
        self.is_deleted = self.id
        self.deleted_at = timezone.now()
        self.cascade = cascade
        self.save()
        models.signals.post_delete.send(sender=self.__class__, instance=self)
        self.delete_related_objects()

    @transaction.atomic
    def restore(self, cascade=False):
        """ 单个恢复"""
        self.is_deleted = -1
        self.deleted_at = None
        self.cascade = cascade
        self.save()
        self.after_restore()
        self.restore_related_objects()

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def after_delete(self):
        pass

    def after_restore(self):
        pass

    def delete_related_objects(self):
        relates = get_candidate_relations_to_delete(self._meta)

        def get_related_queryset(related_model, field, instance):
            return related_model.objects.filter(**{field.name: instance.pk})

        for related in relates:
            for obj in process_relates(related, self, get_related_queryset):
                obj.delete(cascade=True)

    def restore_related_objects(self):
        relates = get_candidate_relations_to_delete(self._meta)

        def get_related_queryset(related_model, field, instance):
            return related_model.deleted_objects.filter(**{field.name: instance.pk, 'cascade': True})

        for related in relates:
            for obj in restore_process_relates(related, self, get_related_queryset):
                obj.restore()
