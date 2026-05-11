from django.contrib.auth.models import User
from rest_framework import serializers
from kan_mind.models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class BoardCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)

    class Meta:
        model = Board
        fields = ['title', 'owner', 'members']

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        user = self.context['request'].user
        board = Board.objects.create(owner=user, **validated_data)
        board.members.set(members)
        print(board)
        return board
