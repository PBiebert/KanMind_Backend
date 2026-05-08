from rest_framework.response import Response
from rest_framework import generics
from kan_mind.models import Board
from .serializers import BoardSerializer, BoardCreateSerializer
from django.contrib.auth.models import User


class BoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BoardCreateSerializer(data=request.data)
        print([user.id for user in User.objects.all()])
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        # serializer.save()
