from rest_framework import serializers

from .models import Agent, Category, Property, PropertyImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'name', 'email', 'phone', 'photo', 'bio', 'agency']


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'caption', 'order']


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    images = PropertyImageSerializer(many=True, read_only=True)
    main_image = serializers.ImageField(required=False)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'price', 'deal_type',
            'area_sqm', 'rooms', 'address', 'latitude', 'longitude',
            'main_image', 'is_active', 'created_at', 'updated_at',
            'owner', 'agent', 'category', 'images',
        ]
        read_only_fields = ['created_at', 'updated_at']
