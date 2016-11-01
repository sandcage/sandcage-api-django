from django.test import LiveServerTestCase
from selenium import webdriver

class SeleniumTestCase(LiveServerTestCase):

    def setUp(self):
        self.client = webdriver.PhantomJS()

    def case_for_all_functions(self, address, should_find):
        # Navigate to the get ingo page
        self.client.get(self.live_server_url + address)

        # Find the submit button
        btn = self.client.find_element_by_xpath("//*[@class='btn btn-primary']")
        btn.click()

        # Get all list elements
        lis = self.client.find_elements_by_tag_name("li")

        # Extract all text attributes
        texts = []
        for li in lis:
            texts.append(li.text)

        # The response without correct apikey should have
        # an error code 1001 (missing key)
        if should_find:
            self.assertTrue('code: 1001' in texts)
        else:
            self.assertFalse('code: 1001' in texts)

    def _test_info(self):
        self.case_for_all_functions('/apigui/info', True)

    def _test_files(self):
        self.case_for_all_functions('/apigui/files', True)
        
    def _test_tasks(self):
        self.case_for_all_functions('/apigui/tasks', False)
        
    def _test_destroy(self):
        self.case_for_all_functions('/apigui/destroy', True)

    def _test_set_key(self):
        self.client.get(self.live_server_url + '/apigui/apikey')
        # Set apikey
        apikey_input = self.client.find_element_by_id("id_apikey")
        apikey_input.send_keys('test')

        # Find the submit button
        btn = self.client.find_element_by_xpath("//*[@class='btn btn-primary']")
        response = btn.click()

    def test_all(self):
        # Needed to be run in this order
        self._test_info()
        self._test_files()
        self._test_tasks()
        self._test_destroy()

        # Set missing apikey to invalid apikey
        self._test_set_key()
        # Let's set key and test info again (code should change to 1003)
        self.case_for_all_functions('/apigui/info', False)
