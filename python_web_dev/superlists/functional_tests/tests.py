from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import unittest
import time
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

# class NewVistorTest(unittest.TestCase):
class NewVistorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		try:
			table = self.browser.find_element_by_id('id_list_table')
			rows = table.find_elements_by_tag_name('tr')
			self.assertIn(row_text, [row.text for row in rows])
		except (AssertionError, WebDriverException) as e:
			if time.time() - start_time > MAX_WAIT:
				raise e
			time.sleep(0.5)

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
		self.browser.get(self.live_server_url)

		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)


		# She is invited to enter a to-do item straight away
		inputBox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputBox.get_attribute('placeholder'), 
			'Enter a to-do item'
			)

		#She types "Buy peacock Feathers" into the text box
		inputBox.send_keys('Buy peacock feathers')

		#When she hits enter, the page updates, and now the page lists "1. Buy peacock feathers" as an item in to-do list table
		inputBox.send_keys(Keys.ENTER)
		# time.sleep(10)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		inputBox = self.browser.find_element_by_id('id_new_item')
		#She types "Use peacock feathers to make a fly" into the text box
		inputBox.send_keys('Use peacock feathers to make a fly')

		#When she hits enter, the page updates, and now the page lists "1. Buy peacock feathers" as an item in to-do list table
		inputBox.send_keys(Keys.ENTER)
		# time.sleep(10)



		# table = self.browser.find_element_by_id('id_list_table')
		# rows = table.find_elements_by_tag_name('tr')
		# self.assertTrue(
		# 	any(row.text == "1. Buy peacock feathers" for row in rows), f"New to-do item did not appear in table. Contents were:\n{table.text}"
		# )
		# self.assertIn('1: Buy Peacock feathers', [row.text for row in rows])
		# self.assertIn('2. User Peacock feathers to make a fly', [row.text for row in rows])
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

		#There is still a text box inviting her to add another To Do item. She enters "Use peacock feather to make fly"
		self.fail("Finish the test")