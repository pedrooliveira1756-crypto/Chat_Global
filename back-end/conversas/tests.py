import json

from django.test import Client, TestCase, override_settings


class FrontendApiTests(TestCase):
    def test_separate_frontend_can_create_user_and_exchange_json_messages(self):
        client = Client(enforce_csrf_checks=True)
        origin = 'http://127.0.0.1:5500'

        preflight = client.options(
            '/chat/create_user/',
            HTTP_ORIGIN=origin,
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='POST',
        )
        self.assertEqual(preflight.status_code, 204)
        self.assertEqual(preflight['Access-Control-Allow-Origin'], origin)

        created = client.post(
            '/chat/create_user/',
            data=json.dumps({'username': 'Ana'}),
            content_type='application/json',
            HTTP_ORIGIN=origin,
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created['Content-Type'], 'application/json')
        self.assertEqual(created['Access-Control-Allow-Origin'], origin)

        sent = client.post(
            '/chat/messages/',
            data=json.dumps({
                'user_id': created.json()['id'],
                'token': created.json()['token'],
                'content': 'Olá!',
            }),
            content_type='application/json',
            HTTP_ORIGIN=origin,
        )
        self.assertEqual(sent.status_code, 201)
        self.assertEqual(sent.json()['content'], 'Olá!')

        received = client.get('/chat/messages/', HTTP_ORIGIN=origin)
        self.assertEqual(received.status_code, 200)
        self.assertEqual(received['Content-Type'], 'application/json')
        self.assertEqual(received.json()[0]['user_id'], created.json()['id'])

    @override_settings(
        ALLOWED_HOSTS=['127.0.0.1', '192.168.1.10'],
        FRONTEND_ORIGINS=[],
        DEBUG=True,
    )
    def test_frontend_on_same_lan_host_can_access_api(self):
        client = Client(enforce_csrf_checks=True)
        host = '192.168.1.10:8000'
        origin = 'http://192.168.1.10:5500'

        preflight = client.options(
            '/chat/create_user/',
            HTTP_HOST=host,
            HTTP_ORIGIN=origin,
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='POST',
        )
        self.assertEqual(preflight.status_code, 204)
        self.assertEqual(preflight['Access-Control-Allow-Origin'], origin)

        created = client.post(
            '/chat/create_user/',
            data=json.dumps({'username': 'Bia'}),
            content_type='application/json',
            HTTP_HOST=host,
            HTTP_ORIGIN=origin,
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created['Access-Control-Allow-Origin'], origin)

        unrelated = client.get(
            '/chat/messages/',
            HTTP_HOST=host,
            HTTP_ORIGIN='http://192.168.1.99:5500',
        )
        self.assertNotIn('Access-Control-Allow-Origin', unrelated)

    def test_message_requires_token_and_invalid_input_returns_json(self):
        client = Client()
        created = client.post(
            '/chat/create_user/',
            data=json.dumps({'username': 'Ana'}),
            content_type='application/json',
        ).json()

        denied = client.post(
            '/chat/messages/',
            data=json.dumps({'user_id': created['id'], 'content': 'Fingindo ser Ana'}),
            content_type='application/json',
        )
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(denied['Content-Type'], 'application/json')

        invalid = client.post(
            '/chat/create_user/', data='não é json', content_type='application/json'
        )
        self.assertEqual(invalid.status_code, 400)
        self.assertEqual(invalid['Content-Type'], 'application/json')

    @override_settings(
        DEBUG=False,
        ALLOWED_HOSTS=['chat.example.com'],
        SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'),
        SECURE_SSL_REDIRECT=True,
    )
    def test_health_endpoint_works_behind_https_proxy(self):
        response = self.client.get(
            '/chat/health/',
            HTTP_HOST='chat.example.com',
            HTTP_X_FORWARDED_PROTO='https',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    @override_settings(
        DEBUG=False,
        ALLOWED_HOSTS=['chat-realtime-api-1nul.onrender.com'],
        FRONTEND_ORIGINS=['https://chatglobal-front-end.vercel.app'],
        SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'),
        SECURE_SSL_REDIRECT=True,
    )
    def test_vercel_origin_can_call_render_api(self):
        client = Client(enforce_csrf_checks=True)
        headers = {
            'HTTP_HOST': 'chat-realtime-api-1nul.onrender.com',
            'HTTP_ORIGIN': 'https://chatglobal-front-end.vercel.app',
            'HTTP_X_FORWARDED_PROTO': 'https',
        }
        preflight = client.options('/chat/create_user/', **headers)
        self.assertEqual(preflight.status_code, 204)
        self.assertEqual(preflight['Access-Control-Allow-Origin'], headers['HTTP_ORIGIN'])

        response = client.get('/chat/messages/', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response['Access-Control-Allow-Origin'], headers['HTTP_ORIGIN'])
