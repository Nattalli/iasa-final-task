from rest_framework import serializers


class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField()
    source = serializers.CharField()
    date = serializers.DateTimeField()
    description = serializers.CharField()
    short_content = serializers.CharField()
    author = serializers.CharField()
    link = serializers.URLField()
    keywords = serializers.ListField(child=serializers.CharField())
    behavior = serializers.CharField()


class GeneralAnalysisSerializer(serializers.Serializer):
    trends = serializers.ListField(child=serializers.CharField())
    general_behavior = serializers.DictField()
    count = serializers.CharField()
    prediction = serializers.CharField()
