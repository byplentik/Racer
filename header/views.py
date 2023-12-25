from django.views import generic
from django.urls import reverse_lazy

from header.models import QuestionsModel
from header.forms import AskQuestionForm


class HomePageTemplateView(generic.TemplateView):
    template_name = 'header/home.html'


class QuestionsListView(generic.ListView):
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


class AskQuestionFormView(generic.FormView):
    form_class = AskQuestionForm
    template_name = 'header/AskQuestionFormView.html'
    success_url = reverse_lazy('zadat_question')

    def form_valid(self, form):
        # Сохранение данных в базу данных
        form.save()
        return super().form_valid(form)