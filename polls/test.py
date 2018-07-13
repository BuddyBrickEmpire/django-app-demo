from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.http import HttpRequest
from django.test import TestCase
import splinter
from polls.views import PollView


class PollViewTest(TestCase):

    fixtures = ['poll']

    def test_get_index(self):
        view = PollView()
        response = view.get(HttpRequest())

        expected = '<li><a href="?id=1">What is your favourite beer type?</a></li>'
        self.assertContains(response, expected)

    def test_get_detail(self):
        view = PollView()
        request = HttpRequest()
        request.GET = {'id': 1}
        response = view.get(request)

        expected = '<input type="radio" name="answer" value="1"'
        self.assertContains(response, expected)

    def test_get_404(self):
        view = PollView()
        request = HttpRequest()
        request.GET = {'id': 99}
        response = view.get(request)

        self.assertEqual(404, response.status_code)

    def test_post(self):
        view = PollView()
        request = HttpRequest()
        request.method = 'POST'
        request.GET = {'id': 1}
        request.POST = {'answer': 1}
        response = view.post(request)

        self.assertEqual(302, response.status_code)
        self.assertEqual('/', response.__getitem__('Location'))

    def test_post_invalid(self):
        view = PollView()
        request = HttpRequest()
        request.method = 'POST'
        request.GET = {'id': 1}
        request.POST = {'answer': -1}
        response = view.post(request)

        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'error')

    def test_post_404(self):
        view = PollView()
        request = HttpRequest()
        request.method = 'POST'
        request.GET = {'id': 99}
        request.POST = {'answer': 1}
        response = view.post(request)

        self.assertEqual(404, response.status_code)


class SeleniumPollTest(StaticLiveServerTestCase):

    fixtures = ['poll']

    def test_flow(self):
        browser = splinter.Browser('chrome', headless=True)
        browser.driver.set_window_size(1900, 1200)

        browser.visit(self.live_server_url)
        browser.driver.save_screenshot('screenshots/1.png')

        browser.find_by_css('li a').first.click()

        browser.driver.save_screenshot('screenshots/2.png')
        self.assertEqual(self.live_server_url + '/?id=1', browser.driver.current_url)

        browser.find_by_css('input[type="radio"]').first.click()
        browser.find_by_css('button').first.click()

        self.assertEqual(self.live_server_url + '/', browser.driver.current_url)

