from rest_framework import serializers
from projects.models import Project, Tag, Review
from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    # owner = ProfileSerializer(many=False)
    # project = ProjectSerializer(many=False)
    class Meta:
        model = Review
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews  = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'


    def get_reviews(self, obj):
        reviews = obj.project_reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data