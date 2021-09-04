from rest_framework import serializers
from rest_framework import validators
from watchlist_app.models import WatchList,StreamPlateform,Review


class ReviewSerializer(serializers.ModelSerializer): 
    review_user = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('watchlist',)
         
class WatchListSerializer(serializers.ModelSerializer):
    reviews = serializers.StringRelatedField(read_only = True, many=True)
    # plateform = serializers.CharField(source = 'plateform.name')

    # def create(self, validated_data):
    #         return WatchList.objects.create(**validated_data)
    class Meta:
        model = WatchList
        fields = '__all__'

class StreamPlateformSerializer(serializers.ModelSerializer):
    
    # nested serialization
    # watchlist =  WatchListSerializer(many=True, read_only=True)
    watchlist = serializers.StringRelatedField(many=True, read_only=True)
   
    class Meta:
        model = StreamPlateform
        fields = '__all__'






   










# validator : it is a core argument that we need to pass to the field
# def name_length(value):
#     if len(value) < 4:
#             raise serializers.ValidationError("too short")
         

# class WatchListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators = [name_length])
#     desc = serializers.CharField()
#     active = serializers.BooleanField()

    # to handle post request, validated_data = data which is entered by the user
    # def create(self, validated_data):
    #     return WatchList.objects.create(**validated_data)

    # to handle put request, instance = original data,  validated_data = updated data
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.desc = validated_data.get('desc', instance.desc)
    #     instance.active = validated_data.get('active', instance.active)
    #     instance.save()
    #     return instance
    
    # oject level validator
    # def validate(self,data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("title and desc same")
    #     else:
    #         return data

    # field level validator
    # def validate_name(self,value):
    #     if len(value) < 4:
    #         raise serializers.ValidationError("too short")
    #     else:
    #         return value      
