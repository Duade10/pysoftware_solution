from django.db import models


class AbstractTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SubjectCategoryMapping(AbstractTimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subjects(AbstractTimeStampModel):
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class Answers(AbstractTimeStampModel):
    text = models.CharField(max_length=1)

    def __str__(self):
        return self.text


class Question(AbstractTimeStampModel):
    SEVERITY = [
        ("1", "Basic"),
        ("2", "Medium"),
        ("3", "High"),
        ("4", "Advanced"),
        ("5", "Highest")
    ]

    category = models.ForeignKey(SubjectCategoryMapping, on_delete=models.CASCADE)
    multiple_quiz_use_subject = models.ManyToManyField(Subjects, related_name="quiz_questions")
    question_severity = models.CharField(null=True, blank=True, max_length=1, choices=SEVERITY)
    question_preamble = models.TextField(help_text="Any preamble or Information needed for the main question",
                                         default="", null=True, blank=True)
    question_main = models.TextField(help_text="Question", null=True, blank=True, max_length=50000)
    question_set_by = models.CharField(max_length=200)
    question_authorised_by = models.CharField(max_length=200, null=True, blank=True)
    question_ready_for_review = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    authorised_date = models.DateTimeField(null=True, blank=True)
    year_of_past_question = models.DateField(null=True, blank=True)
    question_label = models.CharField(max_length=1000, blank=True, null=True)

    # Multiple choice options
    a = models.TextField(null=True, blank=True)
    b = models.TextField(null=True, blank=True)
    c = models.TextField(null=True, blank=True)
    d = models.TextField(null=True, blank=True)
    e = models.TextField(null=True, blank=True)

    hidden = models.BooleanField(default=False)
    explanation = models.TextField(null=True, blank=True)
    answer = models.ManyToManyField(Answers)
    assessment_weight = models.PositiveSmallIntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)
