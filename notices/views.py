from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notice
from .forms import NoticeForm
from accounts.mixins import TeacherMixin, InstitutionAdminMixin

class NoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'notices/list.html'
    context_object_name = 'notices'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        qs = Notice.objects.filter(institution=user.institution, is_active=True).order_by('-created_at')
        if user.role == 'student':
            from django.db.models import Q
            qs = qs.filter(Q(class_ref=user.class_ref) | Q(class_ref__isnull=True))
        return qs

class NoticeCreateView(LoginRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'notices/form.html'
    success_url = reverse_lazy('notice_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.institution = self.request.user.institution
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

class NoticeDeleteView(LoginRequiredMixin, DeleteView):
    model = Notice
    success_url = reverse_lazy('notice_list')
    template_name = 'notices/confirm_delete.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'teacher':
            return qs.filter(posted_by=self.request.user)
        elif self.request.user.role in ['inst_admin', 'super_admin']:
            return qs.filter(institution=self.request.user.institution)
        return qs.none()
