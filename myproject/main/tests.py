from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Orders, UserSearch, Favorites, Ordercomresponsible, Orderresponsible
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
        self.assertEqual(response.json()['count'], 0)

    def test_filter_orders_by_search_query_no_match(self):
        self.user.search.search = 'TestOrderNotFound'
        self.user.search.save()

        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'],
                         0)

    def test_filter_orders_with_search_and_count(self):
        self.user.search.search = 'Test'
        self.user.search.save()

        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'],
                         2)

    def test_all_orders_search(self):
        self.user.search.search = 'order'
        self.user.search.save()

        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 3)

    def test_goals(self):
        Orders.objects.create(name="goals Order 1", goal=True)
        Orders.objects.create(name="goals Order 2", goal=False)
        Orders.objects.create(name="goals Order 3", goal=True)

        self.user.search.goal = True
        self.user.search.save()
        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_favorites(self):
        o1 = Orders.objects.create(name="favorite Order 1")
        Orders.objects.create(name="not favorite Order 2")
        o3 = Orders.objects.create(name="favorite Order 3")
        Favorites.objects.create(user=self.user, order=o1)
        Favorites.objects.create(user=self.user, order=o3)

        self.user.search.favorite = True
        self.user.search.save()
        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_manager(self):
        manager = User.objects.create_user(username="test manager", password="testpass")
        self.user.search.manager = manager
        self.user.search.save()

        order1 = Orders.objects.create(name="First order")
        order2 = Orders.objects.create(name="Second order")
        order3 = Orders.objects.create(name="Third order")

        Orderresponsible.objects.create(user=manager, orderid=order1)
        Orderresponsible.objects.create(user=manager, orderid=order2)

        Ordercomresponsible.objects.create(user=manager, orderid=order1)
        Ordercomresponsible.objects.create(user=manager, orderid=order2)
        Ordercomresponsible.objects.create(user=manager, orderid=order3)

        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 3)

    def test_stage(self):
        Orders.objects.create(name="stage Order 1", stageid=1)
        Orders.objects.create(name="stage Order 2", stageid=2)
        Orders.objects.create(name="stage Order 3", stageid=1)

        self.user.search.stage = 1
        self.user.search.save()
        response = self.client.get(reverse('order_list'), {'action': 'count'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)