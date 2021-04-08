import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models


class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet_address = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nft_id = models.CharField(max_length=64)
    nft_address = models.CharField(max_length=64)
    ipns = models.CharField(max_length=64, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    owner = models.ForeignKey(
        'Artist', null=True, on_delete=models.SET_NULL, related_name='item'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Sign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=128)
    sig = models.CharField(max_length=512)
    version = models.CharField(max_length=3)
    ipns = models.CharField(max_length=64, blank=True)
    type = models.CharField(max_length=64)
    item = models.ForeignKey(
        'Item', null=True, on_delete=models.SET_NULL, related_name='item'
    )
    msg = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
