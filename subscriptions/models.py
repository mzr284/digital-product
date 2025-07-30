from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.validators import SKUValidator

class Package(models.Model):
    title = models.CharField(_("title"), max_length=20)
    sku = models.CharField(_("stock keeping unit"), max_length=20, validators=[SKUValidator], db_index=True)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    price = models.PositiveIntegerField(_("price"))
    duration = models.DurationField(_("duration"), blank=True, null=True)
    is_enable = models.BooleanField(_("is enable"), default=True)

    class Meta:
        db_table = "packages"
        verbose_name = _("package")
        verbose_name_plural = _("packages")

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey('users.User', verbose_name=_("user"), related_name="%(class)s", on_delete=models.CASCADE)
    package = models.ForeignKey(Package, verbose_name=_("package"), related_name="%(class)s", on_delete=models.CASCADE)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    expire_time = models.DateTimeField(_("expire time"), blank=True, null=True)

    class Meta:
        db_table = "subscriptions"
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")

    def __str__(self):
        return f"{self.package.title} for {self.user.username}"

