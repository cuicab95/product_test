from rest_framework import serializers
from ..models import Order, Customer, OrderDetail, ProductProvider, Product, Provider


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class ProductProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProvider
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(ProductProviderSerializer, self).to_representation(instance)
        representation['product'] = ProductSerializer(instance.product, many=False).data
        representation['provider'] = ProviderSerializer(instance.provider, many=False).data
        return representation


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(OrderDetailSerializer,self).to_representation(instance)
        representation['product_provider'] = ProductProviderSerializer(instance.product_provider, many=False).data
        representation['total'] = instance.total
        representation['sale_price'] = f'{instance.sale_price:,}'
        return representation


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(OrderSerializer,self).to_representation(instance)
        representation['customer'] = CustomerSerializer(instance.customer, many=False).data
        representation['detail'] = OrderDetailSerializer(OrderDetail.objects.filter(order_id=instance.id), many=True).data
        representation['timestamp'] = instance.timestamp.strftime("%d/%b/%Y %H:%M:%S")
        representation['total'] = f'{instance.total:,}'
        if instance.assortment_date:
            representation['assortment_date'] = instance.assortment_date.strftime("%d %m %Y %H:%M:%S")
        return representation


class CreateOrderSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    is_urgent = serializers.BooleanField(default=False)
    type = serializers.CharField(max_length=2, required=True)
    items = serializers.JSONField(required=True, allow_null=False)
    additional_data = serializers.JSONField(required=True, allow_null=False)


class FilterOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    is_urgent = serializers.BooleanField(default=False)
    is_assortment = serializers.BooleanField(default=False)
    type = serializers.CharField(max_length=2, required=False)
    customer_type = serializers.CharField(max_length=3, required=False)