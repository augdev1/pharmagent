import uuid
import json
import os
import logging
from django.conf import settings
from django.views.decorators.http import require_GET
from .agent_logic import get_agent_response
from . import agent_logic
from agno.agent import Agent
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from chat.models import Conversation

logger = logging.getLogger(__name__)

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
        try:
            user_message = request.POST.get('userMessage', '')
            image_file = request.FILES.get('image', None)
            image_path = None

            if image_file:
                upload_dir = os.path.join(settings.BASE_DIR, 'chat', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)

                ext = os.path.splitext(image_file.name)[1]
                filename = f"{uuid.uuid4()}{ext}"
                image_path = os.path.join(upload_dir, filename)

                with open(image_path, 'wb+') as destination:
                    for chunk in image_file.chunks():
                        destination.write(chunk)

            conversation = get_object_or_404(Conversation, id=conversation_id)
            agent_response = get_agent_response(user_message, conversation_id, image_path=image_path)

            conversation.history.append({'sender': 'user', 'text': user_message})
            conversation.history.append({'sender': 'bot', 'text': agent_response})
            if not conversation.title and len(conversation.history) > 1:
                conversation.title = conversation.history[1]['text'][:50] + '...' if conversation.history[1]['sender'] == 'user' else conversation.history[0]['text'][:50] + '...'
            conversation.save()

            return JsonResponse({"agentResponse": agent_response})
        except Exception:
            logger.exception("Erro no endpoint get_response para conversation_id=%s", conversation_id)
            return JsonResponse(
                {"error": "Erro interno ao processar a mensagem. Tente novamente em instantes."},
                status=500
            )
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def delete_chat(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    conversation.delete()
    return redirect('new_chat')


@require_GET
def healthcheck(request):
    run_llm = request.GET.get('run_llm') == '1'
    run_ocr = request.GET.get('run_ocr') == '1'
    sample_image = request.GET.get('image_path')

    tesseract_cmd = os.getenv("TESSERACT_CMD", "")
    tessdata_prefix = os.getenv("TESSDATA_PREFIX", "")
    ocr_lang = os.getenv("OCR_LANG", "por")

    checks = {
        "env": {
            "groq_api_key_set": bool(os.getenv("GROQ_API_KEY")),
            "tesseract_cmd_set": bool(tesseract_cmd),
            "tesseract_cmd_exists": bool(tesseract_cmd) and os.path.exists(tesseract_cmd),
            "tessdata_prefix_set": bool(tessdata_prefix),
            "ocr_lang": ocr_lang,
        },
        "llm": {
            "model_init_ok": False,
            "live_call_ok": None,
            "error": None,
        },
        "ocr": {
            "live_check_ok": None,
            "sample_image": sample_image,
            "error": None,
        },
    }

    status_code = 200

    try:
        model = agent_logic.get_llm_model()
        checks["llm"]["model_init_ok"] = model is not None
        if run_llm:
            response = Agent(model=model).run("Responda apenas: OK")
            content = str(getattr(response, "content", "")).strip()
            checks["llm"]["live_call_ok"] = bool(content)
            if not checks["llm"]["live_call_ok"]:
                status_code = 503
    except Exception as e:
        checks["llm"]["error"] = str(e)
        checks["llm"]["live_call_ok"] = False if run_llm else None
        status_code = 503

    if run_ocr:
        if not sample_image:
            checks["ocr"]["error"] = "Forneça image_path para teste OCR real."
            checks["ocr"]["live_check_ok"] = False
            status_code = 400
        else:
            try:
                text = agent_logic.extract_text_from_image(sample_image)
                checks["ocr"]["live_check_ok"] = bool(text and not str(text).startswith("Erro"))
                if not checks["ocr"]["live_check_ok"]:
                    checks["ocr"]["error"] = str(text)[:300]
                    status_code = 503
            except Exception as e:
                checks["ocr"]["live_check_ok"] = False
                checks["ocr"]["error"] = str(e)
                status_code = 503

    checks["ok"] = status_code == 200
    return JsonResponse(checks, status=status_code)