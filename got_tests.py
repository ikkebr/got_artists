import os
import unittest
import got_artists
import json


class SearchTestCase(unittest.TestCase):

    def setUp(self):
        self.client = got_artists.app.test_client()

    def test_user_can_reach_form(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.data)

    def test_post_with_no_values_renders_index(self):
        resp = self.client.post()
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.data)

    def test_post_with_one_value_renders_index(self):
        resp = self.client.post('/', data={'min_age': 10})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.data)

        resp = self.client.post('/', data={'max_age': 10})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.data)

    def test_post_with_invalid_range_renders_index(self):
        resp = self.client.post('/', data={'min_age': 10, 'max_age': -10})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.data)

        resp = self.client.post('/', data={'min_age': -10, 'max_age': 10})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.data)

    def test_post_with_valid_values_shows_no_form(self):
        resp = self.client.post('/', data={'min_age': 0, 'max_age': 90})
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn("form", resp.data)

    def test_post_with_valid_values_returns_valid_json(self):
        resp = self.client.post('/', data={'min_age': 0, 'max_age': 90})
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(json.loads(resp.data), list)

    def test_fitness_function(self):
        a = got_artists.Artists(uuid='foo', age=10)
        b = got_artists.Artists(uuid='bar', age=15)
        c = got_artists.Artists(uuid='blaz', age=20)
        target = got_artists.Search()

        a.age, b.age, c.age = 3, 14, 20
        target.min_age = 0
        target.max_age = 20
        mock_list = [b, a, c]
        self.assertEqual(
            mock_list, sorted(mock_list, key=target.search_fitness))

        a.age, b.age, c.age = 20, 90, 50
        target.min_age = 0
        target.max_age = 90
        mock_list = [c, a, b]
        self.assertEqual(
            mock_list, sorted(mock_list, key=target.search_fitness))


if __name__ == '__main__':
    unittest.main()
