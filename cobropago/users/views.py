from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from common.permissions import IsOwnerOrReadOnly
from .models import User
from .serializers import CreateUserSerializer, UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Creates, Updates, and retrives User accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateUserSerializer
        self.permission_classes = (AllowAny,)
        return super(UserViewSet, self).create(request, *args, **kwargs)

    @list_route(methods=['get'])
    def me(self, request, format=None):
        if not request.user.is_anonymous:
            content = {
                'id': str(request.user.id),
                'username': str(request.user.username)
            }
            return Response(content)
        else:
            raise NotAuthenticated('You are not authenticated')
