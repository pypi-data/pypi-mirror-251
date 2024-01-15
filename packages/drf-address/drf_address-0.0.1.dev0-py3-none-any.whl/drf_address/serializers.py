from rest_framework import serializers
from .models import Address, Country

class CountryRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value.name)
    
    def to_internal_value(self, value):
        return Country.objects.get(code=value)
    

class AddressSerializer(serializers.ModelSerializer):
    country = CountryRelatedField(queryset = Country.objects.all(), required=True)
    
    class Meta:
        model = Address
        fields = "__all__"

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"