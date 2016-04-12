import unittest
from .test_base import TestBase
from .fixtures import ZIPS


class ZipsTest(TestBase):
    def test_admin_crud(self):
        h = self.basic_auth_headers('admin', self.app.config['ADMIN_PASSWORD'])

        item_inserted, status = self.post('_admin/zips', data=ZIPS[0], headers=h)
        self.assertEquals(201, status)

        data, status = self.get('_admin/zips', headers=h)
        self.assertEquals(200, status)

        data, status = self.get('_admin/zips', item_inserted['_id'], headers=h)
        self.assertEquals(200, status)

    def test_public_zips(self):
        h = self.basic_auth_headers('admin', self.app.config['ADMIN_PASSWORD'])
        data, status = self.get('_admin/zips', headers=h)
        self.assertEquals(200, status)

if __name__ == '__main__':
    unittest.main()
