import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Model
# View
class QuestionMondelTests(TestCase):

    def setUp(self):
        self.question = Question(question_text = "Quién es el mejor CD de Platzi ?")

    def test_was_published_recentrly_with_future_question(self):
        #Was_publised_recently return False for questions whose pub_date is in the future
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)
    
    
    def test_was_published_recentrly_with_present_question(self):
        #Was_publised_recently return True for questions whose pub_date is in the present
        time = timezone.now() - datetime.timedelta(hours = 23)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)
    

    def test_was_published_recentrly_with_past_question(self):
        #Was_publised_recently return False for questions whose pub_date is in the past
        time = timezone.now() - datetime.timedelta(days = 1, seconds = 1)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)


def create_question(question_text, days):
    """
    Create a question with the given "question_text" and published the
    given number of days, hours, minutes and seconds offset to now (negative for
    questions published in the past, positive for questions that have 
    yet to be published). 
    """
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):

    def test_no_quetions(self):
        # if no question exist, an appropiate message is displayed
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are avaliable')
        self.assertQuerysetEqual(response.context['lates_question_list'], [])


    def test_future_question(self):
        """
        Question with a pub_date in the future aren´t displayed on the index page. 
        """
        create_question("future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are avaliable')
        self.assertQuerysetEqual(response.context['lates_question_list'], [])


    def test_past_question(self):
        """
        Question with a pub_date in the past aren´t displayed on the index page. 
        """
        question = create_question("past question", days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lates_question_list'], [question])
    
    def test_future_question_and_past_question(self):
        """ 
        Even if both past ant future question exist, only past question are displayed
        """
        past_question = create_question("past question", days=-30)
        future_question =  create_question("future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context["lates_question_list"],
            [past_question]
        )

    def test_two_past_question(self):
        """
        The questions index page may display multiple questions
        """
        past_question1 = create_question("past question 1 ", days=-30)
        past_question2 =  create_question("past question 2", days=-40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context["lates_question_list"],
            [past_question1, past_question2]
        )
    
    def test_two_future_question(self):
        """
        The questions index page may display multiple questions
        """
        future_question1 =  create_question("future question 1", days=30)
        future_question2 =  create_question("future question 2", days=40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context["lates_question_list"],
            []
        )


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 error not found
        """
        future_question =  create_question("future question 1", days=30)
        url = reverse("polls:detail", args= (future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question´s text
        """
        past_question =  create_question("past question", days=-30)
        url = reverse("polls:detail", args= (past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)