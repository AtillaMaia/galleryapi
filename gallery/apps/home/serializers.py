from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from .models import Post, Comments


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username',
                                         read_only=True)
    class Meta:
        model = Comments
        fields = '__all__'


class HomeSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()
    likes = serializers.SlugRelatedField(slug_field='username', many=True,
                                         read_only=True)
    comments = serializers.SlugRelatedField(slug_field='id', many=True,
                                            read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'owner', 'photo', 'approved', 'likes', 'liked',
                  'comments']

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_liked(self, obj):
        return True if obj.likes.filter(id=self.context['request'].user.id) else False

    def to_representation(self, instance):
        data = super(HomeSerializer, self).to_representation(instance)

        data['owner'] = instance.owner.username
        if len(data['comments']) > 0:
            data['comments'] = CommentSerializer(instance.comments.all(),
                                                 many=True).data
        return data


class UploadImageSerializer(HomeSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ['id', 'owner', 'photo', 'approved', 'likes', 'liked',
                  'comments']

    def create(self, validated_data):
        if validated_data['owner'].is_staff:
            data = validated_data.copy()
            data.pop('approved')
            return Post.objects.create(approved=True, **data)
        return Post.objects.create(**validated_data)


class CommentViewSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(),
                                              required=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    message = serializers.CharField(max_length=1000, required=True,
                                    allow_blank=False, allow_null=False)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'post', 'message']

    def create(self, validated_data):
        return Comments.objects.create(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(allow_empty_file=False, required=True)
    approved = serializers.BooleanField(required=True)
    likes = serializers.ListField(child=serializers.CharField(),
                                  allow_empty=True, required=True)

    liked = serializers.BooleanField(required=True)
    comments = CommentSerializer(many=True, required=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'photo', 'approved', 'likes', 'liked',
                  'comments']