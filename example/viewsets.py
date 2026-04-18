from rest_framework import viewsets, permissions
from .models import User,  HistoricoTesouro
from .serializers import UserSerializer, HistoricoTesouroSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


        
        
class HistoricoTesouroViewSet(viewsets.ModelViewSet):
    queryset = HistoricoTesouro.objects.all()
    serializer_class = HistoricoTesouroSerializer

    def get_permissions(self):
        # only authenticated users can list/create/edit their own
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]