from django.db import models

from paymeback.core.models import BaseModel
from paymeback.users.models import User


class Charge(BaseModel):
    title = models.CharField('título', max_length=255)
    debtor_name = models.CharField('nome do devedor', max_length=255)
    loan_date = models.DateTimeField('data do empréstimo')
    date_to_receive = models.DateTimeField('data à receber')
    value = models.DecimalField('valor', max_digits=9, decimal_places=2)
    debtor_phone = models.CharField('telefone do devedor', max_length=20, blank=True)
    details = models.TextField('detalhes', blank=True)
    paid = models.BooleanField('pago', default=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='charges', verbose_name='dono'
    )
    debtor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='debts',
        verbose_name='devedor',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'cobranças'
        verbose_name = 'cobrança'
        ordering = ('-created',)

    def __str__(self):
        return self.title
