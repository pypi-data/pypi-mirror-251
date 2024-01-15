from collections import UserList
from email.utils import parseaddr

from django.core.validators import validate_email, ValidationError
from django.db.models.fields import CharField, TextField
from django.utils.translation import gettext_lazy as _


def validate_email_address(value: str):
    name, address = parseaddr(value)
    if not name and not address:
        raise ValidationError(_("Could not parse email address"))
    validate_email(address)


class EmailField(CharField):
    default_validators = [validate_email_address]
    description = _("Email address")

    def __init__(self, *args, **kwargs):
        # max_length=254 to be compliant with RFCs 3696 and 5321
        kwargs.setdefault("max_length", 254)
        super().__init__(*args, **kwargs)


class MultiEmail(UserList):

    def __str__(self):
        return self.as_string

    @property
    def as_string(self):
        return '\n'.join(self.data)

    @classmethod
    def from_string(cls, value):
        return cls(list(filter(None, value.split('\n'))))


def validate_multi_email_address(value: MultiEmail):
    for email in value:
        validate_email_address(email)


def multi_email_to_python(value):
    if isinstance(value, MultiEmail):
        return value
    elif isinstance(value, (list, tuple)):
        return MultiEmail(list(value))

    return MultiEmail.from_string(value)


class MultiEmailDescriptor:

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # The instance dict contains whatever was originally assigned in
        # __set__.
        if self.field.name in instance.__dict__:
            value = instance.__dict__[self.field.name]
        else:
            instance.refresh_from_db(fields=[self.field.name])
            value = getattr(instance, self.field.name)
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = self.to_python(value)

    def to_python(self, value):
        return multi_email_to_python(value)


class MultiEmailField(TextField):
    descriptor_class = MultiEmailDescriptor

    description = _("Multiple emails")

    default_validators = [validate_multi_email_address]

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Perform preliminary non-db specific value checks and conversions.
        """
        return value.as_string if isinstance(value, MultiEmail) else value

    def from_db_value(self, value, expression, connection):
        return MultiEmail.from_string(value)

    def to_python(self, value):
        return multi_email_to_python(value)

    def contribute_to_class(self, cls, name, *args, **kwargs):
        super().contribute_to_class(cls, name, *args, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))
