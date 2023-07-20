import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import StreamerCard
from payments.business_logic import payout_logic
from django.views.decorators.csrf import csrf_exempt


class PayoutApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        payout_status = payout_logic(request)
        data = {
            'payout_status': payout_status
        }
        return Response(data)


@login_required
@csrf_exempt
def SetDefaultPayoutMethodApi(request):
    if request.method == 'POST':
        payout_method = json.loads(request.body)
        if StreamerCard.objects.filter(streamer__user=request.user, default_payout=True).exists():
            default_streamer_card = StreamerCard.objects.get(streamer__user=request.user, default_payout=True)
            default_streamer_card.default_payout = False
            default_streamer_card.save()
        streamer_card = StreamerCard.objects.get(streamer__user=request.user, type_payout=payout_method)
        streamer_card.default_payout = True
        streamer_card.save()
        return HttpResponse(payout_method)

    return HttpResponse('Method not allowed', status=405)

