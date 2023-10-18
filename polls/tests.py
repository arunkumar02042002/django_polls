import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse
from django.http import HttpResponse

# Create your tests here.
class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now()-datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text: str, days: float) -> Question:
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        """
        If no question exist, an appropriate message is displayed.
        """
        response: HttpResponse = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")

        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Question with pub_date in the past are displayed on the index page.
        """
        question = create_question(question_text="Past Question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question],)

    # def test_future_question(self):
    #     """
    #     Questions with pub_date in the future aren't displayed on the index page.
    #     """
    #     create_question(question_text="Future Question.", days=30)
    #     response = self.client.get(reverse("polls:index"))
    #     print(response.content)
    #     print(response.context['latest_question_list'])
    #     self.assertContains(response, "No polls are available.")
    #     self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are displayed.
        """
        question1 = create_question(question_text="Past Question.",  days=-30)
        create_question(question_text="Future Question.", days=30)
        response = self.client.get(reverse('polls:index'))
        print(response.content)
        print(response.context['latest_question_list'])
        self.assertQuerySetEqual(response.context['latest_question_list'], [question1],)

    def test_two_past_question(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        print(response.content)
        print(response.context['latest_question_list'])
        self.assertQuerySetEqual(response.context['latest_question_list'], [question2, question1],)