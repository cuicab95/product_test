from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import CreateOrderSerializer, OrderSerializer, FilterOrderSerializer
from ..models import Order, Customer
from django.shortcuts import get_object_or_404
from ...global_functions import save_order_detail, validate_structure_order_detail, validate_additional_data


class CreateOrderView(APIView):
    """
    APIView de pedidos
    """
    serializer_class = CreateOrderSerializer

    def get(self, request):
        """
        API para el listado de productos
        :param request:
        :return: objeto de pedidos
        """
        serializer = FilterOrderSerializer(data=request.query_params)
        try:
            kwargs = {}
            if serializer.is_valid():
                is_urgent = serializer.validated_data.get('is_urgent', None)
                order_type = serializer.validated_data.get('order_type', None)
                customer_type = serializer.validated_data.get('customer_type', None)
                is_assortment = serializer.validated_data.get('is_assortment', None)
                if is_urgent:
                    kwargs['is_urgent'] = is_urgent
                if order_type:
                    kwargs['type'] = order_type
                if customer_type:
                    kwargs['customer__type'] = customer_type
                if is_assortment:
                    kwargs['assortment_date__isnull'] = False
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            queryset = Order.objects.filter(**kwargs)
            data = OrderSerializer(queryset, many=True).data
            return Response({'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        API para crear un nuevo pedido
        :param request:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                customer = get_object_or_404(Customer, id=serializer.validated_data['customer_id'])
                is_urgent = serializer.validated_data['is_urgent']
                order_type = serializer.validated_data['type']
                items = serializer.validated_data['items']
                additional_data = serializer.validated_data['additional_data']

                is_correct, message = validate_additional_data(order_type, additional_data) # Validar información adicional
                if not is_correct:
                    return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

                is_correct, message = validate_structure_order_detail(items) # Validar estructura de items
                if not is_correct:
                    return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

                new_order = Order()
                new_order.customer = customer
                new_order.is_urgent = is_urgent
                new_order.type = order_type
                new_order.custom_data = additional_data
                new_order.save()

                # Set items
                is_correct, message = save_order_detail(new_order.id, items) # guardar items y monto total
                if not is_correct:
                    new_order.delete()
                    return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
                data = OrderSerializer(new_order, many=False).data
                return Response({'data': data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
