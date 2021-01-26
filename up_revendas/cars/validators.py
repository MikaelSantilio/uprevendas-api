from django.core.validators import RegexValidator


def validateCarLicensePlate(license_plate):
    error_messages = {
        'invalid_1': "Placa inválida",
        'invalid_2': "Placa padrão Mercosul inválida",
    }

    # regexLicensePlate = RegexValidator(regex=r'^[a-zA-Z]{3}[0-9]{4}$', message=error_messages["invalid_1"])
    regexLicensePlateMercosul = RegexValidator(
        regex=r'^[a-zA-Z]{3}[0-9]{1}[a-zA-Z]{1}[0-9]{2}$', message=error_messages["invalid_2"])

    regexLicensePlateMercosul.__call__(license_plate)

    return license_plate
