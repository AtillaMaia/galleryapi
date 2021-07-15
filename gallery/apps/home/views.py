from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import Post
from .serializers import UploadImageSerializer, HomeSerializer, \
    CommentViewSerializer, PostSerializer


class HomeView(GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = HomeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(approved=True)

    @swagger_auto_schema(responses={status.HTTP_200_OK: PostSerializer(
        many=True)})
    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True,
                                           context={'request': request} )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UploadView(GenericAPIView):
    serializer_class = UploadImageSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: PostSerializer})
    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if not request.user.is_staff:
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApproveView(GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = HomeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, *args, **kwargs):
        filter_ = {}
        for field in [self.lookup_field]:
            filter_[field] = self.kwargs[field]

        obj = get_object_or_404(self.get_queryset(), **filter_)
        return obj

    @swagger_auto_schema(responses={status.HTTP_200_OK: PostSerializer})
    def get(self, request, pk=None):
        obj = self.get_object()
        obj.approved = True
        obj.save()
        serializer = self.serializer_class(obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeView(GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = HomeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, *args, **kwargs):
        filter_ = {}
        for field in [self.lookup_field]:
            filter_[field] = self.kwargs[field]

        obj = get_object_or_404(self.get_queryset(), **filter_)
        return obj

    @swagger_auto_schema(responses={status.HTTP_200_OK: PostSerializer})
    def get(self, request, pk=None):
        obj = self.get_object()

        if obj.likes.filter(id=request.user.id):
            obj.likes.remove(request.user)
        else:
            obj.likes.add(request.user)
        serializer = self.serializer_class(obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentView(GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = CommentViewSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, *args, **kwargs):
        filter_ = {}
        for field in [self.lookup_field]:
            filter_[field] = kwargs[field]

        obj = get_object_or_404(self.get_queryset(), **filter_)
        return obj

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: PostSerializer})
    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        obj = self.get_object(pk=serializer.validated_data['post'].id)
        return Response(HomeSerializer(obj, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)