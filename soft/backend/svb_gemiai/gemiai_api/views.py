from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import models  # Импорт модели для сохранения промпта (optional)

@csrf_exempt
def process_prompt(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')

        # Сохранение промпта в базе данных (optional)
        # prompt_obj = models.Prompt(text=prompt)
        # prompt_obj.save()

        # Обработка промпта с помощью функции get_response
        response = get_response(prompt)

        # Отправка ответа пользователю
        return JsonResponse({'response': response})

    else:
        return JsonResponse({'error': 'Неверный метод запроса.'})

# Функция обработки промпта (вставьте свой код)
def get_response(prompt):
    # ... Логика обработки промпта ...
    return 'Ваш ответ на промпт: ' + prompt