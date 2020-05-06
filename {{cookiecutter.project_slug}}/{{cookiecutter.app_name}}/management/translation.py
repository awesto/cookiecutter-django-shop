"""
These serializer mixinins and fields are used exclusively to import the file
``workdir/fixtures/products-meta.json``. They are not intended for general
purpose and can be deleted thereafter.
"""
{% if cookiecutter.use_i18n == 'y' -%}

from parler_rest.serializers import TranslatedFieldsField, TranslatedField, TranslatableModelSerializerMixin

    {%- if cookiecutter.products_model == 'smartcard' %}


class TranslatableModelSerializerMixin(TranslatableModelSerializerMixin):
    def to_internal_value(self, data):
        data = self._swap_translated_data(data)
        return super(TranslatableModelSerializerMixin, self).to_internal_value(data)

    def _swap_translated_data(self, data):
        """
        Swap translated data unassigned to internal fields.
        """
        remaining = set(data.keys()) - set(self.get_fields().keys())
        for field_name in remaining:
            translations = data.pop(field_name, {})
            for language in translations.keys():
                for key, lemma in translations.get(language, {}).items():
                    data.setdefault(key, {})
                    data[key][language] = lemma
        return data

    {% endif -%}

{% else -%}

from rest_framework import serializers


class TranslatableModelSerializerMixin(object):
    """
    Pseudo class mimicking the behaviour of :class:`parler_rest.TranslatableModelSerializerMixin`.
    It converts the content for fields of type TranslatedFieldsField to simple serializer
    fields.
    """
    def to_internal_value(self, data):
        data = self._unify_translated_data(data)
        result = super(TranslatableModelSerializerMixin, self).to_internal_value(data)
        return result

    def _unify_translated_data(self, data):
        """
        Unify translated data to be used by simple serializer fields.
        """
        for field_name, field in self.get_fields().items():
            if isinstance(field, TranslatedFieldsField):
                key = field.source or field_name
                translations = data.pop(key, None)
                if isinstance(translations, dict):
                    data.update(translations.get('en', {}))
        return data


class TranslatedFieldsField(serializers.Field):
    """
    Pseudo class mimicking the behaviour of :class:`parler_rest.TranslatedFieldsField`, where only
    the English translation is used.
    """
    def to_representation(self, value):
        raise NotImplementedError(
            "If USE_I18N is False, do not use {cls}.to_representation() for field '{field_name}'. "
            "It thwarts the possibility to reuse that string in a multi language environment.".format(
                cls=self.__class__.__name__,
                field_name=self.field_name,
            )
        )

    def validate_empty_values(self, data):
        raise serializers.SkipField()


class TranslatedField(serializers.Field):
    """
    Pseudo class mimicking the behaviour of :class:`parler_rest.TranslatedField`, where only
    the English translation is used.
    """
    def to_representation(self, value):
        raise NotImplementedError(
            "If USE_I18N is False, do not use {cls}.to_representation() for field '{field_name}'. "
            "It thwarts the possibility to reuse that string in a multi language environment.".format(
                cls=self.__class__.__name__,
                field_name=self.field_name,
            )
        )

    def to_internal_value(self, data):
        return data.get('en')
{% endif %}

__all__ = ['TranslatedFieldsField', 'TranslatedField', 'TranslatableModelSerializerMixin']
