from rest_framework.fields import ChoiceField
from timezone_field.rest_framework import TimeZoneSerializerField
from timezone_field.backends import get_tz_backend


class TimeZoneSerializerChoiceField(TimeZoneSerializerField, ChoiceField):
    def __init__(self, **kwargs):
        self.use_pytz = kwargs.pop('use_pytz', None)
        self.tz_backend = get_tz_backend(use_pytz=self.use_pytz)
        super().__init__([(tz, tz) for tz in self.tz_backend.base_tzstrs], **kwargs)
