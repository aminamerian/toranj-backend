from django.urls import reverse
from ..views import CategoryList, ProductList, PriceChangeList, ProductCreate


def test_paginated_response(factory, db):
    path = reverse('core:category_list')
    view = CategoryList.as_view()
    request = factory.get(path)
    response = view(request)
    assert response.status_code == 200
    assert all(key in response.data for key in ['next', 'prev', 'count', 'results'])


def test_category_list_response(factory, leaf_categories):
    path = reverse('core:category_list')
    view = CategoryList.as_view()
    request = factory.get(path)
    response = view(request)
    assert response.status_code == 200
    results = response.data['results']
    # test category list response to have all required values
    # root category has no parent in the response
    assert all(key in results[0] for key in ['id', 'name'])
    assert all(key in results[1] for key in ['id', 'name', 'parent_id'])


def test_category_list_pagination(factory, root_category, middle_category, leaf_categories):
    page_size = 2
    path = reverse('core:category_list')
    view = CategoryList.as_view()
    request = factory.get(path, {'page': 1, 'size': page_size})
    response = view(request)
    assert response.status_code == 200
    assert response.data['count'] == len(leaf_categories) + 2
    assert len(response.data['results']) == page_size


def test_product_list_response(factory, products):
    path = reverse('core:product_list')
    view = ProductList.as_view()
    request = factory.get(path)
    response = view(request)
    assert response.status_code == 200
    assert response.data['count'] == len(products)
    results = response.data['results']
    # test product response to have all required field
    assert all(key in results[0] for key in ['uid', 'product_redirect_url', 'product_price_list_url',
                                             'shop_name', 'name', 'price', 'is_available', 'updated'])


def test_product_list_price_filter(factory, products):
    price_gt_param = 15
    price_lt_param = 40
    path = reverse('core:product_list')
    view = ProductList.as_view()
    request = factory.get(path, {'price__gt': price_gt_param, 'price__lt': price_lt_param})
    response = view(request)
    assert response.status_code == 200
    prices = [p['price'] for p in response.data['results']]
    # Check all product s' prices to be between price filter params
    assert all(price_gt_param < int(price[:2]) < price_lt_param for price in prices)


def test_product_list_category_filter(factory, products, root_category):
    path = reverse('core:product_list')
    view = ProductList.as_view()
    request = factory.get(path, {'category_id': root_category.id, 'size': 100})
    response = view(request)
    assert len(response.data['results']) == len(products)


def test_product_list_price_sort(factory, products, root_category):
    path = reverse('core:product_list')
    view = ProductList.as_view()
    request = factory.get(path, {'sort': '-price', 'size': 100})
    response = view(request)
    results = response.data['results']
    # remove تومان and comma separator from prices
    prices = [int(p['price'][:-6].replace(',', '')) for p in results]
    assert all(prices[i] >= prices[i + 1] for i in range(len(prices) - 1))


def test_product_price_change_list_response(factory, price_change_logs):
    path = reverse('core:product_price_change_list')
    view = PriceChangeList.as_view()
    request = factory.get(path, {'uid': price_change_logs[0].product.uid, 'size': 100})
    response = view(request)
    assert response.status_code == 200
    assert response.data['count'] == len(price_change_logs)
    results = response.data['results']
    # test price change list response to have all required values
    assert all(key in results[0] for key in ['old_price', 'new_price', 'old_availability',
                                             'new_availability', 'price_change_time'])


def test_product_price_change_list(factory, price_change_logs):
    path = reverse('core:product_price_change_list')
    view = PriceChangeList.as_view()
    request = factory.get(path, {'uid': price_change_logs[0].product.uid, 'size': 100})
    response = view(request)
    assert response.status_code == 200
    results = response.data['results']
    new_values = [[p['new_price'], p['new_availability']] for p in results]
    old_values = [[p['old_price'], p['old_availability']] for p in results]
    assert all(new_values[i] == old_values[i - 1] for i in range(1, len(price_change_logs)))
