from rest_framework import serializers

from .models import Eula, EulaFile


class EulaFileSerializer(serializers.ModelSerializer):
    url = serializers.FileField(source='eula_file')

    class Meta:
        model = EulaFile
        fields = ('locale', 'url')


class EulaSerializer(serializers.ModelSerializer):
    urls = EulaFileSerializer(source='eula_files', many=True, read_only=True)

    class Meta:
        model = Eula
        fields = ('valid_from', 'urls')
