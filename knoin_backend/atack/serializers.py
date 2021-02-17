from rest_framework import serializers

from atack.models import Album, Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        print(tracks_data)
        album = Album.objects.create(**validated_data)
        print(album)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album
