from .models import *
from rest_framework import serializers


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = '__all__'

class ComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelComplain
        fields = '__all__'

class ChannelUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelUsers
        fields = '__all__'

class Complain2Serializer(serializers.ModelSerializer):
    ChannelUser = ChannelUserSerializer(many=True)
    class Meta:
        model = ChannelComplain
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelComplainComment
        fields = '__all__'

class Channel2Serializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True,many=True, source='channelcomplain_set')
    class Meta:
        model = Channel
        fields = '__all__'