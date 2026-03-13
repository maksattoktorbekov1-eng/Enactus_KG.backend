from rest_framework import serializers
from django.utils.text import slugify
from .models import News, NewsTranslation, NewsCategory, NewsCategoryTranslation


class NewsCategoryTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategoryTranslation
        fields = ['lang', 'name']


class NewsCategoryPublicSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = NewsCategory
        fields = ['id', 'slug', 'name']

    def get_name(self, obj):
        lang = self.context.get('lang', 'ru')
        translations = obj.translations.all()
        t = next((t for t in translations if t.lang == lang), None)
        t = t or next((t for t in translations if t.lang == 'ru'), None)
        return t.name if t else obj.slug


class NewsCategoryAdminSerializer(serializers.ModelSerializer):
    translations = NewsCategoryTranslationSerializer(many=True)

    class Meta:
        model  = NewsCategory
        fields = ['id', 'slug', 'translations', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        translations_data = validated_data.pop('translations')
        category = NewsCategory.objects.create(**validated_data)
        for t in translations_data:
            NewsCategoryTranslation.objects.create(category=category, **t)
        return category

    def update(self, instance, validated_data):
        translations_data = validated_data.pop('translations', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for t in translations_data:
            NewsCategoryTranslation.objects.update_or_create(
                category=instance,
                lang=t['lang'],
                defaults={'name': t['name']},
            )
        return instance


class NewsTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = NewsTranslation
        fields = ['lang', 'title', 'excerpt', 'content', 'meta_title', 'meta_description']


class NewsListPublicSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    category = NewsCategoryPublicSerializer(read_only=True)

    class Meta:
        model  = News
        fields = ['id', 'slug', 'cover', 'category', 'published_at', 'title', 'excerpt']

    def _get_translation(self, obj):
        lang = self.context.get('lang', 'ru')
        translations = obj.translations.all()
        t = next((t for t in translations if t.lang == lang), None)
        return t or next((t for t in translations if t.lang == 'ru'), None)

    def get_title(self, obj):
        t = self._get_translation(obj)
        return t.title if t else ''

    def get_excerpt(self, obj):
        t = self._get_translation(obj)
        return t.excerpt if t else ''


class NewsPublicSerializer(NewsListPublicSerializer):
    content = serializers.SerializerMethodField()
    meta_title = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()

    class Meta(NewsListPublicSerializer.Meta):
        fields = NewsListPublicSerializer.Meta.fields + ['content', 'meta_title', 'meta_description',]

    def get_content(self, obj):
        t = self._get_translation(obj)
        return t.content if t else ''

    def get_meta_title(self, obj):
        t = self._get_translation(obj)
        return t.meta_title if t else ''

    def get_meta_description(self, obj):
        t = self._get_translation(obj)
        return t.meta_description if t else ''


class NewsAdminSerializer(serializers.ModelSerializer):
    translations = NewsTranslationSerializer(many=True)

    class Meta:
        model = News
        fields = [
            'id', 'slug', 'cover', 'category',
            'is_published', 'published_at',
            'created_at', 'updated_at',
            'translations',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def validate_translations(self, value):
        langs = [t['lang'] for t in value]
        if 'ru' not in langs:
            raise serializers.ValidationError('Перевод на RU обязателен.')
        if len(langs) != len(set(langs)):
            raise serializers.ValidationError('Дублирующиеся языки.')
        return value

    def create(self, validated_data):
        translations_data = validated_data.pop('translations')
        ru = next(t for t in translations_data if t['lang'] == 'ru')
        validated_data['slug'] = self._generate_slug(ru['title'])

        news = News.objects.create(**validated_data)
        for t in translations_data:
            NewsTranslation.objects.create(news=news, **t)
        return news

    def update(self, instance, validated_data):
        translations_data = validated_data.pop('translations', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for t in translations_data:
            NewsTranslation.objects.update_or_create(
            news=instance,
            lang=t['lang'],
            defaults={k: v for k, v in t.items() if k != 'lang'},)
        return instance

    @staticmethod
    def _generate_slug(title: str) -> str:
        from transliterate import translit
        try:
            latin = translit(title, reversed=True)
        except Exception:
            latin = title
        return slugify(latin)