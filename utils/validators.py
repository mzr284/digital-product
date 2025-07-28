from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class SKUValidator(RegexValidator):
    regex = r'^[a-zA-Z0-9]{6-20}$'
    message = _("SKU must be alphanumeric with 6 to 20 character or number")
    code = _("Invalid_SKU")

