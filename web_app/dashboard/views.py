from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from social_django.models import UserSocialAuth
from users.models import StreamerModel, DonateModel, StreamerCard
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from .business_logic import statistics_logic, withdraw_logic
from payments.forms import PayoutAddForm
from .forms import ChangeProfileForm, ChangeSettingsForm


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ProfileStreamerView(DetailView):
    model = StreamerModel
    template_name = 'dashboard/html/profile.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context.update({
                'backend': UserSocialAuth.objects.get(user=self.request.user).provider
            })
        context.update(kwargs)
        return super().get_context_data(**context)

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
            context.update(statistics_logic(self.request))
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
        return DonateModel.objects.filter(streamer__user=self.request.user, payment__status='succeeded').order_by(
            '-payment__payment_date')


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


@login_required
def create_payout_method(request):
    if request.method == 'POST':
        form = PayoutAddForm(request.POST)
        if form.is_valid():
            if StreamerCard.objects.filter(streamer__user=request.user, type_payout=form.cleaned_data['type_payout']).exists():
                streamer_card = StreamerCard.objects.get(streamer__user=request.user,
                                                         type_payout=form.cleaned_data['type_payout'])
                streamer_card.number_card = form.cleaned_data['number_card']
                streamer_card.save()
                return redirect(reverse('withdraw'))

            StreamerCard.objects.create(streamer=StreamerModel.objects.get(user=request.user),
                                        type_payout=form.cleaned_data['type_payout'],
                                        number_card=form.cleaned_data['number_card'])

    return redirect(reverse('withdraw'))


@login_required
def change_profile(request):
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST)
        if form.is_valid():
            pass
    form = ChangeProfileForm()
    return render(request, 'dashboard/html/change_profile.html', {'form': form})


@login_required
def change_settings(request):
    if request.method == 'POST':
        form = ChangeSettingsForm(request.POST)
        if form.is_valid():
            pass
    form = ChangeSettingsForm()
    return render(request, 'dashboard/html/change_profile.html', {'form': form})
