from rest_framework.response import Response
from rest_framework import generics
from kan_mind.models import Board
from .serializers import BoardSerializer, BoardCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class BoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BoardCreateSerializer(
            data=request.data, context={"request": request})
        print([user.id for user in User.objects.all()])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
