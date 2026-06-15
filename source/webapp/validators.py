from django.core.exceptions import ValidationError


def validate_summary_capital(value):
    if value and not value[0].isupper():
        raise ValidationError(
            'Краткое описание должно начинаться с заглавной буквы.'
        )


def validate_no_placeholder(value):
    if value:
        lowered = value.lower()
        for bad in ('lorem', 'test123'):
            if bad in lowered:
                raise ValidationError(
                    f'Текст не должен содержать заглушку "{bad}".'
                )