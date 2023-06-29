from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import StreamerModel, DonateModel
from dashboard.serializers import StreamerModelSerializer, DonateModelSerializer
from .business_logic import get_statistics_for_last_week


class AccountsDonationsApiView(generics.ListAPIView):
    permission_classes = permissions.IsAdminUser
    queryset = StreamerModel.objects.all()
    serializer_class = StreamerModelSerializer


class DonatesInfoApiView(generics.ListAPIView):
    permission_classes = permissions.IsAdminUser
    queryset = DonateModel.objects.all()
    serializer_class = DonateModelSerializer


class AccountDonationsApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        account = StreamerModel.objects.get(user=request.user)
        serializer = StreamerModelSerializer(account)
        return Response(serializer.data)


class DonatesRelatedStreamerInfoApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        donates = DonateModel.objects.filter(streamer__user=request.user).filter(payment__status='succeeded')
        serializer = DonateModelSerializer(donates, many=True)
        return Response(serializer.data)


class DonatesForWeekApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            'statistics_for_last_week': get_statistics_for_last_week(request.user.username)
        }
        return Response(data)
