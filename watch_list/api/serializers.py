from rest_framework import serializers
from ..models import WatchList, Platform, Review


class ReviewSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class WatchListSerializer(serializers.HyperlinkedModelSerializer):
    # len_name = serializers.SerializerMethodField()
    platform_name = serializers.ReadOnlyField(source="platform.name")
    watchlist_review = ReviewSerialiser(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"

    def get_len_name(self, instance):
        return len(instance.name)

    def validate(self, data):
        if data["title"] == data["description"]:
            raise serializers.ValidationError("Name and title can not be the same")
        return data

    # Field  level validation
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short")
        return value


class PlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist_platform = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = Platform
        fields = "__all__"


#
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     is_active = serializers.BooleanField()
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.description = validated_data.get("description", instance.description)
#         instance.is_active = validated_data.get("is_active", instance.is_active)
#         instance.save()
#         return instance
#
#     #Object level validation
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and title can not be the same")
#         return data
#
#     #Field  level validation
#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short")
#         return value
