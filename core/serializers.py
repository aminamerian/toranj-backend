from django.utils import timezone
from rest_framework import serializers

from .models import Category, Product, Shop
from .services.suggestion_service import SuggestionService


class PriceField(serializers.Field):

    def to_representation(self, value):
        return '{:,} تومان'.format(value)

    def to_internal_value(self, data):
        return data


class PassedDateTimeField(serializers.Field):
    """
    Represent the passed date and time in hours and minutes.
    """

    def to_representation(self, value):
        time_difference = timezone.now() - value
        hours, minutes = divmod(time_difference.total_seconds(), 3600)
        minutes = round(minutes / 60)
        output = ''
        if hours > 0:
            output = f'{int(hours)} ساعت و'
        return f'{output} {minutes} دقیقه پیش'

    def to_internal_value(self, data):
        return data


class ProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    shop_domain = serializers.CharField(write_only=True, required=False)
    price = PriceField(required=False)
    product_redirect_url = serializers.SerializerMethodField()
    product_price_list_url = serializers.SerializerMethodField()
    updated = PassedDateTimeField(source='date_updated', read_only=True)

    class Meta:
        model = Product
        fields = ['uid', 'page_url', 'product_redirect_url', 'product_price_list_url', 'shop_name',
                  'shop_domain', 'name', 'price', 'is_available', 'features', 'updated']

        extra_kwargs = {
            # Disable unique validator for page_url field to let a product to be updated using this field.
            # Without this, if page_url already exists, serializer raise validation error.
            'page_url': {'write_only': True, 'required': True, 'validators': []},
            'name': {'required': False},
            'is_available': {'required': False},
            'features': {'write_only': True, 'required': False},
        }

    def create(self, validated_data):
        data = {
            'page_url': validated_data['page_url'],
            'name': validated_data.get('name'),
            'price': validated_data.get('price'),
            'is_available': validated_data.get('is_available'),
            'features': validated_data.get('features'),
        }

        shop_domain = validated_data.get('shop_domain')
        if shop_domain is not None:
            shop = Shop.objects.get(domain=shop_domain)
            data['shop_id'] = shop.id

        # Filter out data with None value to prevent losing data if it was null.
        data = {k: v for k, v in data.items() if v is not None}
        product, created = Product.objects.update_or_create(page_url=data['page_url'], defaults=data)

        if created:
            # Get category from suggestion service if the product just created.
            product.category_id = SuggestionService.get_suggested_category_id(product.name, product.features)
            product.save()
        return product

    @staticmethod
    def get_product_redirect_url(obj):
        return f'/product/redirect/?uid={obj.uid}'

    @staticmethod
    def get_product_price_list_url(obj):
        return f'/product/price-change/list/?uid={obj.uid}'


class CategorySerializer(serializers.ModelSerializer):
    # This is for changing field name 'parent' to 'parent_id'
    # Change allow_null to True to show null parent ids
    parent_id = serializers.ReadOnlyField(source='parent.id', allow_null=False)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_id']


class PriceChangeLogSerializer(serializers.Serializer):
    old_price = PriceField()
    new_price = PriceField(source='price')
    old_availability = serializers.BooleanField()
    new_availability = serializers.BooleanField(source='is_available')
    price_change_time = PassedDateTimeField(source='date')
