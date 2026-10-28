from rest_framework import permissions, viewsets

from .cache import CachedResponseMixin
from .models import Agent, Category, Property
from .serializers import AgentSerializer, CategorySerializer, PropertySerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class CategoryViewSet(CachedResponseMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class AgentViewSet(CachedResponseMixin, viewsets.ModelViewSet):
    queryset = Agent.objects.all().order_by('id')
    serializer_class = AgentSerializer
    permission_classes = [IsAdminOrReadOnly]


class PropertyViewSet(CachedResponseMixin, viewsets.ModelViewSet):
    queryset = Property.objects.select_related('category', 'owner').prefetch_related('images').order_by('-created_at')
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
