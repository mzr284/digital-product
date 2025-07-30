from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.validators import PhoneNumberValidator


class Gateway(models.Model):
    title = models.CharField(_("title"), max_length=25)
    is_enable = models.BooleanField(_("is enable"), default=True)

    class Meta:
        db_table = "gateways"
        verbose_name = _("gateway")
        verbose_name_plural = _("gateways")

    def __str__(self):
        return self.title



class Payment(models.Model):      # a bridge between client and bank for high security
    STATUS_VOID = 0
    STATUS_PAID = 10
    STATUS_ERROR = 20
    STATUS_CANCELED = 30
    STATUS_REFUNDED = 31
    STATUS_CHOICE = (
        (STATUS_VOID, _("Void")),
        (STATUS_PAID, _("Paid")),
        (STATUS_ERROR, _("Error")),
        (STATUS_CANCELED, _("User Canceled")),
        (STATUS_REFUNDED, _("Refunded")),
    )
    user = models.ForeignKey("users.User", verbose_name=_("user"), related_name='%(class)s', on_delete=models.CASCADE)
    package = models.ForeignKey("subscriptions.Package", verbose_name=_("package"),
                                related_name='%(class)s', on_delete=models.CASCADE)
    gateway = models.ForeignKey(Gateway, verbose_name=_("gateway"), related_name='%(class)s', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(_("price"), default=0)
    status = models.PositiveSmallIntegerField(_("status"), choices=STATUS_CHOICE, default=STATUS_VOID)
    token = models.CharField(_("token"), max_length=25, null=True, blank=True)
    phone_number = models.BigIntegerField(_("phone_number"), blank=True, null=True, validators=[PhoneNumberValidator])

    class Meta:
        db_table = "payments"
        verbose_name = _("payment")
        verbose_name_plural = _("payments")

    def __str__(self):
        return f'{self.package} for {self.user} with {self.gateway}'