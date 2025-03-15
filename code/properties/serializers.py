from rest_framework import serializers
from .models import PropertyCategory, PropertySubCategory, Property,  PropertyImage, Inquiry, Favorite,Amenity

class PropertyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyCategory
        fields = '__all__'

class PropertySubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertySubCategory
        fields = '__all__'

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'icon']
        
class PropertySerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    amenities = AmenitySerializer(many=True)
    class Meta:
        model = Property
        fields = '__all__'

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
