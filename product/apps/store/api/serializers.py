from rest_framework import serializers
from ..models import Order, Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(OrderSerializer,self).to_representation(instance)
        representation['customer'] = CustomerSerializer(instance.customer, context={'request': self.context.get('request')}).data
        return representation


class CreateOrderSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    is_urgent = serializers.BooleanField(default=False)
    type = serializers.CharField(max_length=2, required=True)
    items = serializers.JSONField(required=True, allow_null=False)
    additional_data = serializers.JSONField(required=True, allow_null=False)


class FilterOrderSerializer(serializers.Serializer):
    is_urgent = serializers.BooleanField(default=False)
    is_assortment = serializers.BooleanField(default=False)
    type = serializers.CharField(max_length=2, required=False)
    customer_type = serializers.CharField(max_length=3, required=False)