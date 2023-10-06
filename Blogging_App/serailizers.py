from rest_framework import serializers
from .models import User, Blog, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'first_name', 'last_name']

    def validate(self, attrs):
        user_email = attrs.get('email', None)
        if not user_email:
            raise serializers.ValidationError("Email is empty")
        queryset = User.objects.filter(email=user_email)
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise serializers.ValidationError({'email': 'Email is already in use'})
        return attrs

    def create(self, validated_data):
        poped = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(poped)
        user.save()
        user = User.objects.filter(id=user.id).first()
        return user


class BlogCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment',)

    def create(self, **validated_data):
        data = Blog.objects.create(**validated_data)
        print(validated_data)
        return data


class BlogSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField(required=False)
    total_comments = serializers.SerializerMethodField(required=False)
    blog_comments = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Blog
        fields = ['id', 'user', 'title', 'posted_date', 'blog', 'is_active', 'total_likes', 'total_comments',
                  'blog_comments']

    def create(self, validated_data):
        data = Blog.objects.create(**validated_data)
        print(validated_data)
        return data

    def update(self, instance, validated_data):
        print("Hello From Blog Update")
        Blog.objects.filter(id=instance.id).update(**validated_data)
        instance = Blog.objects.filter(id=instance.id).first()
        return instance

    def get_total_likes(self, obj):
        return Comment.objects.filter(blog=obj.id, is_liked=True, is_active=True).count()

    def get_total_comments(self, obj):
        return Comment.objects.filter(blog=obj.id, is_comment=True, is_active=True).count()

    def get_blog_comments(self, obj):
        comment = Comment.objects.filter(blog=obj.id, is_comment=True, is_active=True)[:5]
        return BlogCommentsSerializer(comment, many=True).data if comment else None


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'blog', 'comment', 'is_active', 'is_comment', 'is_liked']

    def validate(self, attrs):
        user = attrs.get('user', None)
        blog = attrs.get('blog', None)
        is_comment = attrs.get('is_comment', None)
        is_liked = attrs.get('is_liked', None)
        if not is_comment:
            context = Comment.objects.filter(user=user, blog=blog, is_liked=True, is_comment=False, is_active=True)
            print("Existing", context)
            if context.exists():
                print("Hello")
                raise serializers.ValidationError({'user': 'User already liked this post'})
            return attrs
        elif not is_comment and not is_liked:
            context = Comment.objects.filter(user=user, blog=blog, is_liked=False, is_comment=False, is_active=True)
            print("Existing", context)
            if context.exists():
                raise serializers.ValidationError({'user': 'User has not liked this post post'})
            return attrs
        if is_comment:
            return attrs

    def create(self, validated_data):
        data = Comment.objects.create(**validated_data)
        return data

    def update(self, instance, validated_data):
        print("Hello From Blog Update")
        Blog.objects.filter(id=instance.id).update(**validated_data)
        instance = Blog.objects.filter(id=instance.id).first()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['email', 'password']
