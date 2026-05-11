from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Q
from django.contrib.auth import get_user_model
from kan_mind.models import Board
from .serializers import BoardSerializer

User = get_user_model()


class BoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def list(self, request):
        user = self.request.user
        queryset = Board.objects.filter(
            Q(owner=user) | Q(members=user)).distinct()
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BoardSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
