import json
import hashlib
import hmac
import secrets

from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Message, user


def health(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except DatabaseError:
        return JsonResponse({'status': 'unavailable'}, status=503)
    return JsonResponse({'status': 'ok'})


def json_object(request):
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = json_object(request)
        username = data.get('username') if data else None
        if not isinstance(username, str) or not 0 < len(username.strip()) <= 100:
            return JsonResponse({'error': 'Nome inválido (máximo de 100 caracteres).'}, status=400)
        username = username.strip()

        token = secrets.token_urlsafe(32)
        usuario = user.objects.create(
            username=username,
            token_hash=hashlib.sha256(token.encode()).hexdigest(),
        )

        return JsonResponse({
            "id": usuario.id,
            "username": usuario.username,
            "token": token,
        }, status=201)

    return JsonResponse({
        "error": "Método não permitido"
    }, status=405)


@csrf_exempt
def messages(request):

    # GET - buscar mensagens
    if request.method == "GET":
        messages = reversed(list(Message.objects.select_related('user').order_by('-id')[:200]))

        data = []

        for message in messages:
            data.append({
                "id": message.id,
                "user_id": message.user_id,
                "username": message.user.username,
                "content": message.content
            })

        return JsonResponse(data, safe=False)


    # POST - enviar mensagem
    if request.method == "POST":
        data = json_object(request)
        user_id = data.get('user_id') if data else None
        token = data.get('token') if data else None
        content = data.get('content') if data else None
        if type(user_id) is not int or user_id < 1:
            return JsonResponse({'error': 'Usuário inválido.'}, status=400)
        if not isinstance(content, str) or not 0 < len(content.strip()) <= 5000:
            return JsonResponse({'error': 'Mensagem inválida (máximo de 5000 caracteres).'}, status=400)
        usuario = user.objects.filter(id=user_id).first()
        if usuario is None:
            return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)
        if not isinstance(token, str) or not usuario.token_hash or not hmac.compare_digest(
            usuario.token_hash, hashlib.sha256(token.encode()).hexdigest()
        ):
            return JsonResponse({'error': 'Identidade inválida. Entre novamente na conversa.'}, status=403)

        message = Message.objects.create(
            user=usuario,
            content=content.strip()
        )

        return JsonResponse({
            "id": message.id,
            "user_id": message.user_id,
            "username": message.user.username,
            "content": message.content
        }, status=201)


    return JsonResponse({
        "error": "Método não permitido"
    }, status=405)
