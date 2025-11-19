import uuid
import json
import os
from django.conf import settings
from .agent_logic import get_agent_response
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from chat.models import Conversation

def new_chat(request):
    conversation = Conversation.objects.create()
    conversation.history.append({'sender': 'bot', 'text': 'Olá! Sou o Bryan, seu assistente IA de cadastro de receitas! No que posso ajudar hoje?'})
    conversation.save()
    return redirect('index', conversation_id=conversation.id)

def index(request, conversation_id=None):
    if not conversation_id:
        return redirect('new_chat')

    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    conversations = Conversation.objects.exclude(title__isnull=True).exclude(title__exact='').order_by('-created_at')
    
    return render(request, "chat/index.html", {
        'conversation': conversation,
        'conversations': conversations
    })

def get_response(request, conversation_id):
    if request.method == 'POST':
        user_message = request.POST.get('userMessage', '')
        image_file = request.FILES.get('image', None)
        image_path = None

        if image_file:
            # Define o diretório de upload e o cria se não existir
            upload_dir = os.path.join(settings.BASE_DIR, 'chat', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Gera um nome de arquivo único
            ext = os.path.splitext(image_file.name)[1]
            filename = f"{uuid.uuid4()}{ext}"
            image_path = os.path.join(upload_dir, filename)
            
            # Salva o arquivo
            with open(image_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

        conversation = get_object_or_404(Conversation, id=conversation_id)

        agent_response = get_agent_response(user_message, conversation_id, image_path=image_path)

        # Salva o histórico da conversa
        conversation.history.append({'sender': 'user', 'text': user_message})
        conversation.history.append({'sender': 'bot', 'text': agent_response})
        if not conversation.title and len(conversation.history) > 1:
            # Garante que o título seja pego da primeira mensagem do usuário
            conversation.title = conversation.history[1]['text'][:50] + '...' if conversation.history[1]['sender'] == 'user' else conversation.history[0]['text'][:50] + '...'
        conversation.save()

        return JsonResponse({"agentResponse": agent_response})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def delete_chat(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    conversation.delete()
    return redirect('new_chat')