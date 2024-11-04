import re
from datetime import datetime
from typing import List, Dict, Optional

import PyPDF2
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View, UpdateView, DeleteView

from .forms import QuestionUploadForm, QuestionEditForm
from .models import Question, SubjectCategoryMapping, Subjects


def extract_questions(pdf_content: str) -> List[Dict[str, Optional[str]]]:
    """
    Extracts questions from a PDF content string.

    The questions are stored in a list of dictionaries, where each dictionary has
    the following keys:
        'question_main': The main question text.
        'a', 'b', 'c', 'd', 'e': The option text for each option.

    The questions are extracted by looking for lines that start with a number
    followed by a period (e.g. "1. This is a question"). The question text is
    everything after the period. The options are extracted by looking for lines
    that start with a letter (A-E) followed by a period, and the option text is
    everything after the period.

    Args:
        pdf_content: The string content of the PDF file.

    Returns:
        A list of dictionaries, where each dictionary represents a question.
    """

    questions = []
    current_question = None

    for line in pdf_content.split("\n"):

        line = line.strip()

        if not line:
            continue

        if re.match(r'^\d+\.', line):
            if current_question:
                questions.append(current_question)

            question_text = line.split('.', 1)[1].strip()
            current_question = {
                'question_main': question_text,
                'a': None,
                'b': None,
                'c': None,
                'd': None,
                'e': None
            }

        elif line.startswith(('A.', 'B.', 'C.', 'D.', 'E.')):
            option = line[0].lower()
            option_text = line[2:].strip()
            if current_question:
                current_question[option] = option_text

    if current_question:
        questions.append(current_question)

    return questions


class UploadQuestions(View):
    """
    Upload a PDF file containing questions and extract the questions.

    The PDF file should contain the questions in the following format:

    1. Question
    A. Option A
    B. Option B
    C. Option C
    D. Option D
    E. Option E

    The questions will be stored in the session and the user will be redirected
    to the preview page.

    Args:
        The request object.

    Returns:
        The rendered template.
    """

    def get(self, request, *args: List, **kwargs: Dict) -> HttpResponse:
        form = QuestionUploadForm
        return render(request, 'upload.html', {'form': form})

    def post(self, request, *args: List, **kwargs: Dict) -> HttpResponse:
        form = QuestionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_text = "".join(page.extract_text() for page in pdf_reader.pages)
            questions = extract_questions(pdf_text)
            request.session['questions'] = questions
            return redirect('core:preview')
        return render(request, 'upload.html', {'form': form})


class PreviewQuestions(View):
    """
    Preview questions before saving them to the database.

    :param request: The request object.
    :return: The rendered template.
    """

    def get(self, request, *args: List, **kwargs: Dict) -> HttpResponse:
        """Get the questions from the session and render the template."""
        questions = request.session.get('questions', [])
        return render(request, 'preview.html', {'questions': questions})

    def post(self, request, *args: List, **kwargs: Dict) -> HttpResponse:
        """Save the questions from the session to the database."""

        questions = request.session.get('questions', [])
        category, _ = SubjectCategoryMapping.objects.get_or_create(
            name='JAMB',
            defaults={'name': 'JAMB'}
        )
        subject, _ = Subjects.objects.get_or_create(
            text='Principles of Accounting',
            defaults={'text': 'Principles of Accounting'}
        )

        for q in questions:
            question = Question(
                category=category,
                question_main=q['question_main'],
                question_set_by='JAMB',
                year_of_past_question=datetime.now().date(),
                a=q.get('a'),
                b=q.get('b'),
                c=q.get('c'),
                d=q.get('d'),
                e=q.get('e')
            )
            question.save()
            question.multiple_quiz_use_subject.add(subject)
        return redirect('core:question_list')


class QuestionListView(ListView):
    """
    List all questions.
    """
    model = Question
    template_name = 'list.html'
    context_object_name = 'questions'


class QuestionUpdateView(UpdateView):
    """
    View to update a question.
    """
    model = Question
    form_class = QuestionEditForm
    template_name = 'edit.html'
    context_object_name = 'question'

    def get_initial(self):
        """
        Set the category of the question in the initial form data.
        """
        initial = super().get_initial()
        question = self.get_object()
        initial['category'] = question.category
        return initial

    def form_valid(self, form):
        """
        Save the question with the user who modified it and the date.
        """
        question = form.save(commit=False)
        question.question_set_by = 'JAMB'
        question.year_of_past_question = datetime.now().date()
        question.save()
        return redirect('question_list')


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'delete.html'
    context_object_name = 'question'
    success_url = reverse_lazy('core:question_list')
