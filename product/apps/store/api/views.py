from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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

    id_param = openapi.Parameter('id', openapi.IN_QUERY, description="Id del pedido", type=openapi.TYPE_INTEGER)
    is_urgent_param = openapi.Parameter('is_urgent', openapi.IN_QUERY, description="Obtener pedidos urgentes", type=openapi.TYPE_BOOLEAN)
    order_type_param = openapi.Parameter('order_type', openapi.IN_QUERY, description="Tipo de pedido", type=openapi.TYPE_STRING)
    customer_type_param = openapi.Parameter('customer_type', openapi.IN_QUERY, description="Tipo de cliente", type=openapi.TYPE_STRING)
    is_assortment_param = openapi.Parameter('is_assortment', openapi.IN_QUERY, description="Obtener pedidos que no se han surtido", type=openapi.TYPE_BOOLEAN)
    @swagger_auto_schema(operation_description="API para el listado de productos", manual_parameters=[id_param, is_urgent_param, order_type_param, customer_type_param, is_assortment_param], responses={200: 'Success', 400: 'Bad request', 500: 'External error'})
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
                order_id = serializer.validated_data.get('id', None)
                is_urgent = serializer.validated_data.get('is_urgent', None)
                order_type = serializer.validated_data.get('order_type', None)
                customer_type = serializer.validated_data.get('customer_type', None)
                is_assortment = serializer.validated_data.get('is_assortment', None)
                if order_id:
                    kwargs['id'] = order_id
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
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    customer_id_param = openapi.Parameter('customer_id', openapi.IN_QUERY, description="Id del cliente", type=openapi.TYPE_INTEGER)
    is_urgent_param = openapi.Parameter('is_urgent', openapi.IN_QUERY, description="Es pedido urgente", type=openapi.TYPE_BOOLEAN)
    type_param = openapi.Parameter('type', openapi.IN_QUERY, description="Tipo de pedido", type=openapi.TYPE_STRING)
    items_param = openapi.Parameter('items', openapi.IN_QUERY, description="Listado de productos, por ejemplo: [{'product_id': 1, 'quantity': 2}]", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER))
    additional_data_param = openapi.Parameter('additional_data', openapi.IN_QUERY, description="Información adicional, por ejemplo: {'stock': 'Almacen 1'}", type=openapi.TYPE_OBJECT)

    @swagger_auto_schema(operation_description="API para crear un nuevo pedido",
                         manual_parameters=[customer_id_param, is_urgent_param, type_param, items_param, additional_data_param],
                         responses={201: 'Success', 400: 'Bad request', 500: 'External error', 404: 'Not found'})
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
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
