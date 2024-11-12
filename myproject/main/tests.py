from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Orders, UserSearch
import logging


logger = logging.getLogger(__name__)
User = get_user_model()

class OrderListTest(TestCase):
    def setUp(self):
        search_data = UserSearch.objects.create()
        self.user = User.objects.create_user(username='testuser', password='password', search=search_data)
        self.client.force_login(self.user)
        Orders.objects.create(name="Test Order 1", searchowners="Owner 1")
        Orders.objects.create(name="Test Order 2", searchowners="Owner 2")
        Orders.objects.create(name="Another Order", searchowners="Owner 3")

    def test_filter_orders_by_search_query(self):
        self.user.search.search = 'Test'
        self.user.search.save()

        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)  # Проверяем, что количество заказов после фильтрации правильно

    def test_no_orders_found_for_non_matching_search(self):
        self.user.search.search = 'NonMatchingSearch'
        self.user.search.save()

        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)  # Проверяем, что количество заказов равно 0

    def test_filter_orders_by_search_query_no_match(self):
        self.user.search.search = 'TestOrderNotFound'
        self.user.search.save()

        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'],
                         0)  # Проверяем, что заказов не найдено, если фильтрации не происходит

    def test_filter_orders_with_search_and_count(self):
        self.user.search.search = 'Test'
        self.user.search.save()

        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'],
                         2)  # Проверяем, что после фильтрации по "Test" вернется правильное количество заказов

    def test_all_orders_search(self):
        self.user.search.search = 'order'
        self.user.search.save()

        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 3)  # Проверяем, что все заказы возвращаются, если search пустой

    def test_only_first_if_in_else_passes(self):
        Orders.objects.create(name="Test Order 3", goal=True)
        Orders.objects.create(name="Test Order 4", goal=False)
        Orders.objects.create(name="Test Order 5", goal=True)

        self.user.search.goal = True
        self.user.search.save()
        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)
