from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


def validateCarLicensePlate(license_plate):
    error_messages = {
        'invalid': _("Invalid license plate."),
    }
    regexLicensePlate = RegexValidator(regex=r'^[a-zA-Z]{3}[0-9]{4}$', message=error_messages["invalid"])
    regexLicensePlateMercosul = RegexValidator(
        regex=r'^[a-zA-Z]{3}[0-9]{1}[a-zA-Z]{1}[0-9]{2}$', message=error_messages["invalid"])

    regexLicensePlate.__call__(license_plate)
    regexLicensePlateMercosul.__call__(license_plate)

    return license_plate
