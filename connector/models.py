from django.db import models
from django.utils.translation import gettext as _


CONNECTOR = (
    ('SNMP', 'SNMP'),
)


class Parameter(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Parameter Name'))
    connector = models.CharField(max_length=20, choices=CONNECTOR, default='SNMP', verbose_name=_('Connector Type'))
    value = models.CharField(max_length=100, verbose_name=_('Parameter Value'))

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        db_table = 'parameter'
        verbose_name = _('parameter')
        verbose_name_plural = _('parameter list')

    def __str__(self):
        return '%s(%s)' % (self.name, self.connector)

    def save(self):
        self.name = self.name.upper()
        return super(Parameter, self).save()


class Device(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('Device Brand'))
    connector = models.CharField(max_length=20, choices=CONNECTOR, default='SNMP', verbose_name=_('Connector Type'))
    parameter_type = models.ForeignKey(
        Parameter,
        on_delete=models.RESTRICT,
        related_name='parameter_type',
        verbose_name=_('Parameter Device Type'),
        null=True,
        blank=True
    )
    parameter_1 = models.ForeignKey(
        Parameter,
        on_delete=models.RESTRICT,
        related_name='parameter_1',
        verbose_name=_('Parameter 1'),
        null=True,
        blank=True
    )
    parameter_2 = models.ForeignKey(
        Parameter,
        on_delete=models.RESTRICT,
        related_name='parameter_2',
        verbose_name=_('Parameter 2'),
        null=True,
        blank=True
    )
    parameter_3 = models.ForeignKey(
        Parameter,
        on_delete=models.RESTRICT,
        related_name='parameter_3',
        verbose_name=_('Parameter 3'),
        null=True,
        blank=True
    )
    parameter_4 = models.ForeignKey(
        Parameter,
        on_delete=models.RESTRICT,
        related_name='parameter_4',
        verbose_name=_('Parameter 4'),
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        db_table = 'device'
        verbose_name = _('device')
        verbose_name_plural = _('device List')

    def __str__(self):
        return '%s' % self.name

    def save(self):
        self.name = self.name.upper()
        return super(Device, self).save()
