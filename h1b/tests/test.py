import unittest

import h1b


class ServerTests(unittest.TestCase):
    test_client = None

    def setUp(self):
        h1b.app.testing = True
        self.test_client = h1b.app.test_client()

    def tearDown(self):
        pass

    def test_setup(self):
        response = self.test_client.get('/')
        assert response.status_code == 200

    def test_empty_index(self):
        response = self.test_client.get('/')
        assert response.data is not None


if __name__ == '__main__':
    unittest.main()
