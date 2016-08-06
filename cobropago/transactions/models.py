from django.db import models
from django.utils.translation import ugettext as _
from decimal import Decimal
from common.models import CommonModel


class Ledger(CommonModel):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=32, decimal_places=2, default=Decimal('0.00'))

    def set_balance(self):
        balance = self.accounts.aggregate(total=models.Sum('balance')).get('total', Decimal('0'))

        if self.id:
            self.__class__.objects.filter(id=self.id).update(balance=balance)
            self.refresh_from_db()

    def __str__(self):
        return self.name


class WithLedgerModel(CommonModel):
    ledger = models.ForeignKey(Ledger, related_name="%(class)ss")

    class Meta:
        abstract = True
        unique_together = (('user', 'ledger', 'name'),)
        index_together = (('user', 'ledger', 'name'),)


class Account(WithLedgerModel):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=32, decimal_places=2, default=Decimal('0.00'))

    def set_balance(self):
        balance = self.transactions.aggregate(total=models.Sum('amount')).get('total', Decimal('0'))
        if self.id:
            self.__class__.objects.filter(id=self.id).update(balance=balance)
            self.refresh_from_db()

    def __str__(self):
        return self.name + " " + self.user.username


class Payee(WithLedgerModel):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name + " " + self.user.username


class Transaction(WithLedgerModel):
    date = models.DateField(db_index=True)
    check = models.CharField(max_length=30, blank=True)
    account = models.ForeignKey(Account, related_name='transactions')
    payee = models.ForeignKey(Payee, related_name='transactions')
    memo = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=30, decimal_places=2)

    class Meta(CommonModel.Meta):
        unique_together = ()
        index_together = (('user', 'ledger', 'account'),
                          ('user', 'ledger', 'payee'),
                          ('user', 'ledger', 'account', 'payee'))

    def save(self, *args, **kwargs):
        if not (self.ledger.user == self.user):
            raise ValueError(_("The ledger does not belong to the user"))
        if not (self.account.ledger == self.ledger):
            raise ValueError(_("The account does not belong to the ledger"))
        if not (self.payee.ledger == self.ledger):
            raise ValueError(_("The payee does not belong to the ledger"))
        super(Transaction, self).save(*args, **kwargs)
