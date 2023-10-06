# DRF
from rest_framework import serializers

# First party
from games.models import Game


class GameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=11,
        decimal_places=2,
        required=False
    )
    poster = serializers.ImageField(required=False)
    rate = serializers.FloatField(required=False)

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name',
            instance.name
        )
        instance.price = validated_data.get(
            'price',
            instance.price
        )
        instance.rate = validated_data.get(
            'rate',
            instance.rate
        )
        instance.poster = validated_data.get(
            'poster',
            instance.poster
        )
        instance.save()
        return instance


class GameCreateSerializer(serializers.ModelSerializer):
    rate = serializers.FloatField(default=0)

    class Meta:
        model = Game
        fields = [
            'name',
            'price',
            'poster',
            'rate'
        ]


# TODO: Реализовать покупку товара!
