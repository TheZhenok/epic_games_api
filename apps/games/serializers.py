from rest_framework import serializers


class GameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=11, decimal_places=2)
    poster = serializers.ImageField()
