from rest_framework import serializers
from .models import Partner, PartnerTranslation


class PartnerTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PartnerTranslation
        fields = ['lang', 'name']


class PartnerPublicSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()

    class Meta:
        model  = Partner
        fields = ['id', 'name', 'logo', 'website_url', 'sort_order']

    def _get_translation(self, obj):
        lang = self.context.get('lang', 'ru')
        translations = obj.translations.all()
        t = next((t for t in translations if t.lang == lang), None)
        return t or next((t for t in translations if t.lang == 'ru'), None)

    def get_name(self, obj):
        t = self._get_translation(obj)
        return t.name if t else ''


class PartnerAdminSerializer(serializers.ModelSerializer):
    translations = PartnerTranslationSerializer(many=True)

    class Meta:
        model  = Partner
        fields = ['id', 'logo', 'website_url', 'is_active', 'sort_order', 'translations']
        read_only_fields = ['id']

    def validate_translations(self, value):
        langs = [t['lang'] for t in value]
        if 'ru' not in langs:
            raise serializers.ValidationError('Перевод на RU обязателен.')
        if len(langs) != len(set(langs)):
            raise serializers.ValidationError('Дублирующиеся языки.')
        return value

    def create(self, validated_data):
        translations_data = validated_data.pop('translations')
        partner = Partner.objects.create(**validated_data)
        for t in translations_data:
            PartnerTranslation.objects.create(partner=partner, **t)
        return partner

    def update(self, instance, validated_data):
        translations_data = validated_data.pop('translations', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for t in translations_data:
            PartnerTranslation.objects.update_or_create(
                partner=instance,
                lang=t['lang'],
                defaults={'name': t['name']},
            )
        return instance


class PartnerReorderSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text='Список ID партнёров в нужном порядке'
    )