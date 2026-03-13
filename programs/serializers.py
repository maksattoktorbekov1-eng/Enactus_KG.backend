from rest_framework import serializers
from django.utils.text import slugify
from .models import (
    Program, ProgramTranslation,
    ProgramGallery, ProgramTeam,
    ProgramAdvisor, ProgramTimeline,
    ProgramTimelineTranslation,
)


class ProgramTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProgramTranslation
        fields = [
            'lang', 'title', 'description', 'content',
            'instruction', 'meta_title', 'meta_description',
        ]


class ProgramGallerySerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = ProgramGallery
        fields = ['id', 'image', 'caption', 'sort_order']
        read_only_fields = ['id']


class ProgramTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProgramTeam
        fields = ['id', 'name', 'university', 'logo', 'is_active', 'sort_order']
        read_only_fields = ['id']


class ProgramAdvisorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = ProgramAdvisor
        fields = ['id', 'full_name', 'position', 'photo', 'sort_order']
        read_only_fields = ['id']


class ProgramTimelineTranslationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = ProgramTimelineTranslation
        fields = ['lang', 'title', 'description']


class ProgramTimelineSerializer(serializers.ModelSerializer):
    translations = ProgramTimelineTranslationSerializer(many=True)

    class Meta:
        model  = ProgramTimeline
        fields = ['id', 'year', 'sort_order', 'translations']
        read_only_fields = ['id']


    def create(self, validated_data):
        translations_data = validated_data.pop('translations')
        timeline = ProgramTimeline.objects.create(**validated_data)
        for t in translations_data:
            ProgramTimelineTranslation.objects.create(timeline=timeline, **t)
        return timeline


    def update(self, instance, validated_data):
        translations_data = validated_data.pop('translations', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for t in translations_data:
            ProgramTimelineTranslation.objects.update_or_create(
                timeline=instance,
                lang=t['lang'],
                defaults={k: v for k, v in t.items() if k != 'lang'},
            )
        return instance


class ProgramListPublicSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model  = Program
        fields = ['id', 'slug', 'program_type', 'image', 'title', 'description']

    
    def _get_translation(self, obj):
        lang = self.context.get('lang', 'ru')
        translations = obj.translations.all()
        t = next((t for t in translations if t.lang == lang), None)
        return t or next((t for t in translations if t.lang == 'ru'), None)

    
    def get_title(self, obj):
        t = self._get_translation(obj)
        return t.title if t else ''

    
    def get_description(self, obj):
        t = self._get_translation(obj)
        return t.description if t else ''


class ProgramPublicSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    instruction = serializers.SerializerMethodField()
    meta_title = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()
    gallery = ProgramGallerySerializer(many=True, read_only=True)
    teams = ProgramTeamSerializer(many=True, read_only=True)
    advisors = ProgramAdvisorSerializer(many=True, read_only=True)
    timeline = ProgramTimelineSerializer(many=True, read_only=True)

    
    class Meta:
        model  = Program
        fields = [
            'id', 'slug', 'program_type', 'image',
            'title', 'description', 'content', 'instruction',
            'meta_title', 'meta_description',
            'gallery', 'teams', 'advisors', 'timeline',
        ]

    def _get_translation(self, obj):
        lang = self.context.get('lang', 'ru')
        translations = obj.translations.all()
        t = next((t for t in translations if t.lang == lang), None)
        return t or next((t for t in translations if t.lang == 'ru'), None)

    
    def get_title(self, obj):
        t = self._get_translation(obj)
        return t.title if t else ''

    
    def get_description(self, obj):
        t = self._get_translation(obj)
        return t.description if t else ''

    
    def get_content(self, obj):
        t = self._get_translation(obj)
        return t.content if t else ''

    
    def get_instruction(self, obj):
        t = self._get_translation(obj)
        return t.instruction if t else ''

    
    def get_meta_title(self, obj):
        t = self._get_translation(obj)
        return t.meta_title if t else ''

    
    def get_meta_description(self, obj):
        t = self._get_translation(obj)
        return t.meta_description if t else ''



class ProgramAdminSerializer(serializers.ModelSerializer):
    translations = ProgramTranslationSerializer(many=True)
    gallery = ProgramGallerySerializer(many=True, read_only=True)
    teams = ProgramTeamSerializer(many=True, read_only=True)
    advisors = ProgramAdvisorSerializer(many=True, read_only=True)
    timeline = ProgramTimelineSerializer(many=True, read_only=True)

    
    class Meta:
        model  = Program
        fields = [
            'id', 'slug', 'program_type', 'image',
            'is_active', 'sort_order',
            'created_at', 'updated_at',
            'translations',
            'gallery', 'teams', 'advisors', 'timeline',
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

        program = Program.objects.create(**validated_data)
        for t in translations_data:
            ProgramTranslation.objects.create(program=program, **t)
        return program

    
    def update(self, instance, validated_data):
        translations_data = validated_data.pop('translations', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for t in translations_data:
            ProgramTranslation.objects.update_or_create(
                program=instance,
                lang=t['lang'],
                defaults={k: v for k, v in t.items() if k != 'lang'},
            )
        return instance

    
    @staticmethod
    def _generate_slug(title: str) -> str:
        from transliterate import translit
        try:
            latin = translit(title, reversed=True)
        except Exception:
            latin = title
        return slugify(latin)