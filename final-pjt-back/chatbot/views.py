import json
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from deposits.models import DepositProducts as Deposit
from savings.models import SavingProducts as Saving

openai.api_key = ''

@csrf_exempt
def recommend(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=400)
        
        body = json.loads(request.body.decode('utf-8'))
        user_message = body.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'No user message provided'}, status=400)

        # Fetching the top 5 deposit and saving products
        deposits = list(Deposit.objects.values('fin_prdt_nm', 'mtrt_int', 'fin_prdt_cd')[:5])
        savings = list(Saving.objects.values('fin_prdt_nm', 'mtrt_int', 'fin_prdt_cd')[:5])

        # Create a list of product descriptions for the prompt
        deposit_descriptions = "\n".join(
            [f"{d['fin_prdt_nm']}: 금리 {d['mtrt_int']}%, <a href='http://localhost:5173/products/{d['fin_prdt_cd']}/deposit' target='_blank'>상세정보 보기</a>"
             for d in deposits]
        )
        saving_descriptions = "\n".join(
            [f"{s['fin_prdt_nm']}: 금리 {s['mtrt_int']}%, <a href='http://localhost:5173/products/{s['fin_prdt_cd']}/saving' target='_blank'>상세정보 보기</a>"
             for s in savings]
        )

        # Construct the prompt for GPT
        prompt = f"""
        사용자가 다음과 같은 정보를 제공했습니다:
        "{user_message}"

        사용자의 정보와 조건에 맞는 가장 적합한 예금 또는 적금 상품을 추천해 주세요. 
        아래는 추천 가능한 예금 및 적금 상품 목록입니다:

        예금:
        {deposit_descriptions}

        적금:
        {saving_descriptions}
        """

        # Generate a recommendation using GPT-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024
        )

        recommendation = response['choices'][0]['message']['content'].strip()
        formatted_recommendation = recommendation.replace('\n', '<br>')
        return JsonResponse({'recommendation': formatted_recommendation})

    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({'error': str(e)}, status=500)
