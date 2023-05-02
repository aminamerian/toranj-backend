import pytest, random
from rest_framework.test import APIRequestFactory
from mixer.backend.django import mixer

from ..models import Category, Product, PriceChangeLog, Shop


# with scope='module', APIRequestFactory will be instantiated only once per module
@pytest.fixture(scope='module')
def factory():
    return APIRequestFactory()


@pytest.fixture
def root_category(db):
    root_category = mixer.blend(Category, name='گوشی و تبلت')
    return root_category


@pytest.fixture
def middle_category(root_category):
    category = mixer.blend(Category, name='گوشی موبایل', parent=root_category)
    return category


@pytest.fixture
def leaf_categories(middle_category):
    cats = ('آیفون', 'سامسونگ', 'شیائومی', 'ایسوس')
    leaf_categories = mixer.cycle(len(cats)).blend(Category, parent=middle_category, name=(name for name in cats))
    return leaf_categories


@pytest.fixture
def products(db, leaf_categories):
    prices = (12, 43, 10, 17, 32, 25, 73, 11, 39, 40, 15, 67)
    # create a list with length len(price) from categories.
    categories = random.choices(leaf_categories, k=len(prices))
    products = mixer.cycle(len(prices)).blend(
        Product,
        price=(price for price in prices),
        category=(cat for cat in categories),
    )
    return products


@pytest.fixture
def price_change_logs(products):
    price_change_logs = mixer.cycle(10).blend(PriceChangeLog, product=products[0])
    return price_change_logs


@pytest.fixture
def shop(db):
    shop = mixer.blend(Shop, domain="https://digikala.com")
    return shop
