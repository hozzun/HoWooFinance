# import openai
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from deposits.models import DepositProducts as Deposit
# from savings.models import SavingProducts as Saving


# @csrf_exempt
# def recommend(request):
#     try:
#         user_message = request.POST.get('message', '')

#         prompt = f"""
#         사용자가 다음과 같은 정보를 제공했습니다:
#         "{user_message}"

#         사용자가 제공한 정보에 따라 가장 적합한 예금 또는 적금 상품을 추천해 주세요. 조건에 맞는 상품을 선택하고, 금리가 높은 상품을 우선으로 추천해 주세요. 사용 가능한 상품은 다음과 같습니다:

#         예금:
#         """
        
#         deposits = list(Deposit.objects.values('fin_prdt_nm', 'mtrt_int', 'fin_prdt_cd')[:5])
#         savings = list(Saving.objects.values('fin_prdt_nm', 'mtrt_int', 'fin_prdt_cd')[:5])

#         for deposit in deposits:
#             prompt += f"정기예금: {deposit['fin_prdt_nm']}, 금리: {deposit['mtrt_int']}%, 상세정보: <a href='http://localhost:5173/products/{deposit['fin_prdt_cd']}/deposit' target='_blank'>링크</a>\n"
        
#         prompt += "\n적금:\n"

#         for saving in savings:
#             prompt += f"적금: {saving['fin_prdt_nm']}, 금리: {saving['mtrt_int']}%, 상세정보: <a href='http://localhost:5173/products/{saving['fin_prdt_cd']}/saving' target='_blank'>링크</a>\n"

#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful financial assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=1024
#         )

#         recommendation = response['choices'][0]['message']['content'].strip()
#         formatted_recommendation = recommendation.replace('\n', '<br>')
#         return JsonResponse({'recommendation': formatted_recommendation})

#     except Exception as e:
#         print("Error:", str(e))
#         return JsonResponse({'error': str(e)}, status=500)
