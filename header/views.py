from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from header.models import QuestionsModel, ReviewsModel
from header.forms import AskQuestionForm, ReviewForm

from basket.mixins import CreateSessionKeyMixin


class HomePageTemplateView(CreateSessionKeyMixin, generic.TemplateView):
    template_name = 'header/home.html'


class QuestionsListView(CreateSessionKeyMixin, generic.ListView):
    template_name = 'header/QuestionsListView.html'
    model = QuestionsModel
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page')
        if page_number:
            page_title = f"Страница {page_number}"
        else:
            page_title = False
        context['page_title'] = page_title
        return context


class AskQuestionFormView(CreateSessionKeyMixin, generic.FormView):
    form_class = AskQuestionForm
    template_name = 'header/AskQuestionFormView.html'
    success_url = reverse_lazy('zadat_question')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ReviewsListView(CreateSessionKeyMixin, generic.ListView):
    model = ReviewsModel
    template_name = 'header/ReviewsListView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review_form.save()
            return redirect('reviews_view')
        else:
            print(review_form.errors)
            return render(request, self.template_name, {'review_form': review_form, 'object_list': self.get_queryset()})


class VideoTemplateView(CreateSessionKeyMixin, generic.TemplateView):
    template_name = 'header/VideoTemplateView.html'


class ContactsTemplateView(CreateSessionKeyMixin, generic.TemplateView):
    template_name = 'header/ContactsTemplateView.html'
