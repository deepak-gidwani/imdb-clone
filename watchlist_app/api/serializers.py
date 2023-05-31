from rest_framework import serializers
from watchlist_app.models import *

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review 
        # fields = '__all__'
        exclude = ('watchlist',)

class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True,read_only=True) # read-only mtlb post req m reviews ni create krenge bs get m recieve krenge
    # platform = serializers.StringRelatedField() ye sahi kyu ki model m __str__ name de rha h
    # or we can use that
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = "__all__"
        extra_kwargs = {
            "avg_rating":{"read_only": True},
            "number_rating":{"read_only": True}
        }


# class StreamPlatformSerializer(serializers.ModelSerializer): modelserializer
#     watchlist = WatchListSerializer(many=True,read_only=True)  # same name as realted_name in models
#     # watchlist = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name="movie-detail")
#     class Meta:
#         model = StreamPlatform
#         fields = "__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):  
    watchlist = WatchListSerializer(many=True,read_only=True)  # same name as realted_name in models

    class Meta:
        model = StreamPlatform
        fields = "__all__"
    

# class MovieSerializer(serializers.ModelSerializer):
    
#     len_name = serializers.SerializerMethodField() #custom method field
#     class Meta:
#         model = Movie
#         fields = "__all__"
        
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and description should be different")      
#         return data
    
#     def validate_name(self,value): # field level validation
#         if len(value)<3:
#             raise serializers.ValidationError("Name is too short")
#         return value
        
#     def get_len_name(self,value): # field level
#         return len(value.name)
 
# def name_lenth(value):
#     if len(value)<3:
#         raise serializers.ValidationError("Name is too short")
#     return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_lenth]) # validators
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
    
#     def create(request,validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self,data):  # object level validation
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and description should be different")      
#         return data
    
    # def validate_name(self,value): # field level validation
    #     if len(value)<3:
    #         raise serializers.ValidationError("Name is too short")
    #     return value
        