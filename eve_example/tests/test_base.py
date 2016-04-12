import os
import re
os.environ['EVE_SETTINGS'] = re.sub('/venv', '', os.path.abspath('./eve_example/tests/settings.py'))

import unittest
import base64
import json
import eve
from glob import glob
from eve import ISSUES
from flask.ext.pymongo import MongoClient
from bson import ObjectId
from eve_example import eve_example
from datetime import datetime, timedelta


class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = eve_example.app
        self.client = self.app.test_client()
        self.domain = self.app.config['DOMAIN']
        self.setupDb()

    def tearDown(self):
        self.dropDB()
        del self.app

    def setupDb(self):
        self.connection = MongoClient(self.app.config['MONGO_URI'])
        self.db = self.connection.get_default_database()
        self.connection.drop_database(self.db)
        self.bulk_insert()

    def bulk_insert(self):
        files = glob(os.path.join(os.path.dirname(__file__), '../data/*.json'))
        for path in files:
            collection = self.db[os.path.splitext(os.path.basename(path))[0]]
            with open(path, 'r') as fh:
                for line in fh:
                    collection.insert(json.loads(line))

    def dropDB(self):
        self.connection.drop_database(self.app.config['MONGO_DBNAME'])
        self.connection.close()
        self.connection = None

    def epoch(self):
        return datetime(1970, 1, 1)

    def date_now(self):
        return datetime.utcnow().replace(microsecond=0)

    def basic_auth_headers(self, username, password):
        auth = base64.b64encode((username + ':' + password).encode('ascii'))
        return [('Authorization', 'Basic ' + auth.decode('ascii'))]

    def auth(self, user):
        return [('Authorization', 'Bearer %s' % user['token'])]

    def admin_auth(self):
        return self.basic_auth_headers('admin', self.app.config['ADMIN_PASSWORD'])

    def resolve_resource(self, resource, item=None):
        resource_params = []
        if isinstance(resource, tuple):
            resource_params = list(resource[0:-1])
            resource = resource[-1]
        if resource in self.domain:
            resource = self.domain[resource]['url']
            if resource_params:
                resource = re.sub(r'<.*?>', lambda v: str(resource_params.pop()), resource)
        if item:
            if isinstance(item, dict):
                item = item.get('id')
            request = '/%s/%s' % (resource, str(item))
        else:
            request = '/%s' % (resource)
        return request

    def get(self, resource, item=None, query='', headers=[]):
        url = self.resolve_resource(resource, item)
        res = self.client.get(url + query, headers=headers)
        return self.parse_response(res)

    def post(self, resource, data, item=None, headers=[], content_type=None):
        if not content_type:
            content_type = 'application/json'
        headers.append(('Content-Type', content_type))
        url = self.resolve_resource(resource, item)
        res = self.client.post(url, data=json.dumps(data), headers=headers)
        return self.parse_response(res)

    def put(self, resource, data, item=None, headers=[]):
        headers.append(('Content-Type', 'application/json'))
        url = self.resolve_resource(resource, item)
        res = self.client.put(url, data=json.dumps(data), headers=headers)
        return self.parse_response(res)

    def patch(self, resource, data, item=None, headers=[]):
        headers.append(('Content-Type', 'application/json'))
        url = self.resolve_resource(resource, item)
        res = self.client.patch(url, data=json.dumps(data), headers=headers)
        return self.parse_response(res)

    def delete(self, resource, item=None, headers=None):
        url = self.resolve_resource(resource, item)
        res = self.client.delete(url, headers=headers)
        return self.parse_response(res)

    def parse_response(self, res):
        val = None
        if res.get_data():
            val = res.get_data().decode("utf-8")
            try:
                val = json.loads(val)
            except ValueError:
                self.fail("'%s' is not valid JSON" % (val))

        return val, res.status_code

    def create(self, resource, data, user=None):
        if not user:
            user = self.u.john
        data, status = self.post(resource, data, headers=self.auth(user))
        if status != 201:
            print(data)
        self.assertNoError(data)
        return ObjectId(data['_id'])

    def fetch(self, resource, item=None, user=None):
        if not user:
            user = self.u.john
        data, status = self.get(resource, item=item, headers=self.auth(user))
        self.assertNoError(data)
        return data

    def modify(self, resource, item, body, user=None):
        if not user:
            user = self.u.john
        data, status = self.patch(resource, body, item=item,
                                  headers=self.auth(user))
        self.assertNoError(data)
        return data

    def remove(self, resource, item, user=None):
        if not user:
            user = self.u.john
        data, status = self.delete(resource, item,
                                   headers=self.auth(user))
        self.assertNoError(data)

    def assertNoError(self, response):
        if response is None:
            return
        self.assertIsInstance(response, dict)
        if eve.STATUS in response:
            self.assertTrue(eve.STATUS_OK in response[eve.STATUS],
                            'status is not OK: %s' % response)

    def assertValidationError(self, response, matches):
        self.assertTrue(eve.STATUS in response, 'missing status')
        self.assertTrue(eve.STATUS_ERR in response[eve.STATUS],
                        'status is not ERR')
        self.assertTrue(ISSUES in response, 'response as no issues')
        issues = response[ISSUES]
        self.assertTrue(len(issues))

        for k, v in matches.items():
            self.assertTrue(k in issues, 'no "%s" error' % k)
            self.assertTrue(v in issues[k],
                            '"%s" error does not contain "%s"' % (k, v))

    def assertTimeEqual(self, time1, time2):
        self.assertAlmostEqual(time1, time2, delta=timedelta(seconds=10))
