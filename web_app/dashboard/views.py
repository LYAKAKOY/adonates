from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from social_django.models import UserSocialAuth
from users.models import StreamerModel, DonateModel
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from users.forms import ChangeProfileForm, ChangeGoalForm, ChangeSettingsForm
from .business_logic import statistics_logic, withdraw_logic, change_profile_logic


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ProfileStreamerView(DetailView):
    model = StreamerModel
    template_name = 'dashboard/html/profile.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            profileForm = ChangeProfileForm()
            profileForm.fields['username'].initial = self.request.user.username
            goalForm = ChangeGoalForm()
            streamer = StreamerModel.objects.select_related('streamerGoal', 'streamerSettings').get(user=self.request.user)
            goalForm.fields['goal'].initial = streamer.streamerGoal.goal
            goalForm.fields['description'].initial = streamer.streamerGoal.description
            settingsForm = ChangeSettingsForm()
            settingsForm.fields['min_sum_donate'].initial = streamer.streamerSettings.min_sum_donate
            context.update({
                'backend': UserSocialAuth.objects.get(user=self.request.user).provider,
                'profileForm': profileForm,
                'goalForm': goalForm,
                'settingsForm': settingsForm,
            })
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_object(self, queryset=None):
        return StreamerModel.objects.select_related('user').get(user=self.request.user)


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
        return DonateModel.objects.select_related('payment').filter(streamer__user=self.request.user, payment__status='succeeded').order_by(
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


def change_profile(request):
    if request.method == 'POST':
        change_profile_logic(request)
    return redirect(reverse('profile'))