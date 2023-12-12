# validators.py

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.utils import timezone


class SpanishMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ("La contraseña debe tener al menos %(min_length)d caracteres.") % {
                    'min_length': self.min_length},
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_helptext(self):
        return ("La contraseña debe tener al menos %(min_length)d caracteres.") % {'min_length': self.min_length}


class LetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra."), code='password_no_letter')

    def get_help_text(self):
        return _("La contraseña debe contener al menos una letra.")


class UppercaseValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra mayúscula."), code='password_no_uppercase')

    def get_help_text(self):
        return _("La contraseña debe contener al menos una letra mayúscula.")


class OneNumberValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("La contraseña debe contener al menos un número."), code='password_no_number')

    def get_help_text(self):
        return _("La contraseña debe contener al menos un número.")
