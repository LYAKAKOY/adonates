from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from users.models import StreamerModel, DonateModel
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from .business_logic import dashboard_logic, withdraw_logic
from .forms import PayoutForm


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ProfileStreamerView(DetailView):
    model = StreamerModel
    template_name = 'dashboard/html/profile.html'
    context_object_name = 'account'

    def get_object(self, queryset=None):
        return StreamerModel.objects.get(user=self.request.user)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class StatisticsView(DetailView):
    model = StreamerModel
    template_name = 'dashboard/html/statistics.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context.update(dashboard_logic(self.request))
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_object(self, queryset=None):
        return StreamerModel.objects.get(user=self.request.user)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class AllDonationsView(DetailView):
    model = DonateModel
    template_name = 'dashboard/html/donations.html'
    context_object_name = 'donations'

    def get_object(self, queryset=None):
        return DonateModel.objects.filter(streamer__user=self.request.user, payment__status='succeeded')


@method_decorator(login_required(login_url='/login'), name='dispatch')
class WithdrawView(DetailView):
    model = StreamerModel
    template_name = 'dashboard/html/withdraw.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context.update(withdraw_logic(self.request))
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_object(self, queryset=None):
        return StreamerModel.objects.get(user=self.request.user)


def create_payout_method(request):
    if request.method == 'POST':
        form = PayoutForm(request.POST)
        if form.is_valid():
            pass

    return redirect(reverse('withdraw'))
