from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from .serailizers import UserSerializer, LoginSerializer, BlogSerializer, CommentSerializer
from rest_framework.response import Response
from .models import User, Blog, Comment
from django.contrib.auth import login
from .services import get_tokens_for_user
from .pagination import CustomPagination


# Create your views here.
class RegisterView(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super(RegisterView, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset

    @csrf_exempt
    @action(methods=['POST'], detail=False, permission_classes=[AllowAny])
    def users(self, request):
        if request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer = serializer.save()
                return Response(UserSerializer(instance=serializer).data, status=status.HTTP_202_ACCEPTED)
            return Response(UserSerializer(instance=serializer).errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    @action(methods=['GET', 'POST', 'PUT'], detail=False, permission_classes=[IsAuthenticated],
            pagination_class=CustomPagination)
    def blogs(self, request):
        if request.method == 'GET':
            blogs = Blog.objects.filter(is_active=True)
            query = self.filter_queryset(blogs)
            page = self.paginate_queryset(query)
            serializer = BlogSerializer(page, many=True)
            if page is not None:
                return self.get_paginated_response(serializer.data)
            else:
                return Response({'Message': "Null"}, status=status.HTTP_200_OK)
        if request.method == 'POST':
            user = request.user.id
            data = request.data
            data['user'] = user
            serializer = BlogSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer = serializer.save()
                return Response(BlogSerializer(instance=serializer).data, status=status.HTTP_202_ACCEPTED)
            return Response(BlogSerializer(instance=serializer).errors, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'PUT':
            blog_id = request.data.get('id')
            instance = Blog.objects.filter(id=blog_id).first()
            data = request.data
            data['id'] = blog_id
            user = request.user.id
            data = request.data
            data['user'] = user
            serializer = BlogSerializer(instance=instance, data=data)
            serializer.is_valid(raise_exception=True)
            serializer = serializer.save()
            return Response(BlogSerializer(instance=serializer).data, status=status.HTTP_202_ACCEPTED)

    @csrf_exempt
    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated],
            pagination_class=CustomPagination)
    def blog_view(self, request):
        if request.method == 'GET':
            blog_id = self.request.query_params.get('id')
            blogs = Blog.objects.filter(id=blog_id, is_active=True, )
            query = self.filter_queryset(blogs)
            page = self.paginate_queryset(query)
            serializer = BlogSerializer(page, many=True)
            if page is not None:
                return self.get_paginated_response(serializer.data)
            else:
                return Response({'Message': "Null"}, status=status.HTTP_200_OK)

    @csrf_exempt
    @action(methods=['GET', 'POST', 'PUT'], detail=False, permission_classes=[IsAuthenticated],
            pagination_class=CustomPagination)
    def commentviews(self, request):
        if request.method == 'GET':
            comments = Comment.objects.filter(is_active=1)
            # print(blogs)
            query = self.filter_queryset(comments)
            page = self.paginate_queryset(query)
            serializer = BlogSerializer(page, many=True)
            if page is not None:
                return self.get_paginated_response(serializer.data)
            else:
                return Response({'Message': "Null"}, status=status.HTTP_200_OK)

        if request.method == 'POST':
            user = request.user.id
            data = request.data
            data['user'] = user
            serializer = CommentSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer = serializer.save()
                return Response(CommentSerializer(instance=serializer).data, status=status.HTTP_202_ACCEPTED)
            return Response(CommentSerializer(instance=serializer).errors, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'PUT':
            blog_id = request.data.get('id')
            instance = Blog.objects.filter(id=blog_id).first()
            data = request.data
            data['id'] = blog_id
            user = request.user.id
            data = request.data
            data['user'] = user
            serializer = CommentSerializer(instance=instance, data=data)
            serializer.is_valid(raise_exception=True)
            serializer = serializer.save()
            return Response(CommentSerializer(instance=serializer).data, status=status.HTTP_202_ACCEPTED)

    @csrf_exempt
    @action(methods=['POST', 'PUT'], detail=False, permission_classes=[IsAuthenticated],
            pagination_class=CustomPagination)
    def likePost(self, request):
        if request.method == 'POST':
            user = request.user.id
            data = request.data
            data['user'] = user
            serializer = CommentSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer = serializer.save()
                return Response(CommentSerializer(instance=serializer).data, status=status.HTTP_202_ACCEPTED)
            return Response(CommentSerializer(instance=serializer).errors, status=status.HTTP_400_BAD_REQUEST)


class SingleBlogView(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    pagination_class = CustomPagination

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], pagination_class=CustomPagination)
    def single_blog(self, request):
        if request.method == 'GET':
            user = request.user.id
            # blog_id=self.get_object()
            # print(blog_id)
            blogs = Blog.objects.filter(is_active=True, user=user)
            query = self.filter_queryset(blogs)
            page = self.paginate_queryset(query)
            serializer = BlogSerializer(page, many=True)
            if page is not None:
                return self.get_paginated_response(serializer.data)
            else:
                return Response({'Message': "Null"}, status=status.HTTP_200_OK)


class LoginView(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny])
    def login(self, request):
        if request.method == 'POST':
            if request.method == 'POST':
                serializer = LoginSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                email = serializer.data.get('email')
                password = serializer.data.get('password')
                user = User.objects.filter(email=email).first()
                if not user:
                    return Response({'error': "User does not Exist"}, status=status.HTTP_404_NOT_FOUND)
                if user.check_password(password):
                    login(request, user)
                    return Response(
                        {'user': email, 'Message': 'Login Successful', 'token': get_tokens_for_user(user)},
                        status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'error': {'non_fields_errors': ['Username or Password is not valid']}},
                                    status=status.HTTP_401_UNAUTHORIZED)
