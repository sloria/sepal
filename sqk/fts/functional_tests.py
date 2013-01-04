from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from sqk.datasets.factories import DatasetFactory
from nose.tools import assert_equal, assert_in
import time


class DatasetCrudTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.wait = WebDriverWait(self.browser, 10)

    def tearDown(self):
        self.browser.quit()

    def test_dataset_create(self):
        b = self.browser
        root = self.live_server_url
        # Rosie opens her browser and goes to home page
        b.get(root)

        # She sees the title of the page is the brand and tagline
        page_title = b.find_element_by_css_selector('head title')
        assert_equal(u'sepal | Mine your audio', page_title.text)

        # She sees the page header with the brand name
        header = b.find_element_by_class_name('header')
        assert_in('sepal', header.text)

        # TODO: test login here

        # She clicks on the Datasets link
        b.find_element_by_link_text('Datasets').click()
        assert_in("Create", body_text(b))
        assert_in('No datasets', body_text(b))

        # She clicks on the create dataset button
        b.find_element_by_link_text('Create Dataset').click()
        assert_in('New Dataset', body_text(b))
        # She fills in the species field but NOT the name field
        species_field = b.find_element_by_name('species')
        species_field.send_keys('P. californiucus')

        # She clicks submit
        click_submit(b)
        # Oops, she sees an error
        assert_in('This field is required', body_text(b))

        # She fills in a name
        name_field = b.find_element_by_name('name')
        name_field.send_keys('Differences between bonded and unbonded P. Cal USVs')

        # then clicks submit again
        click_submit(b)

        # She is now on the datasets page
        page_title = b.find_element_by_css_selector(".page-title")
        assert_in('Datasets', page_title.text)

        # her newly created dataset is in a table
        dataset_rows = b.find_elements_by_css_selector("table tbody tr")
        assert_in("Differences between bonded", dataset_rows[0].text)
        assert_equal(len(dataset_rows), 1)

    def test_dataset_edit(self):
        # A dataset is created
        dataset = DatasetFactory.build()
        dataset.description = ''
        dataset.save()
        b = self.browser
        # go right to the edit page
        edit_url = self.live_server_url + '/datasets/{}/edit/'.format(dataset.pk)
        # Rosie opens her browser and goes straight to the edit page
        b.get(edit_url)

        # she's now at the edit form
        assert_in('Edit Dataset', body_text(b))

        # she adds a description to the dataset
        desc_field = b.find_element_by_css_selector('#id_description')
        desc_field.send_keys("This is my first dataset.")
        # she clicks submit
        click_submit(b)

        # back to the datasets page.
        page_title = b.find_element_by_css_selector(".page-title")
        assert_in('Datasets', page_title.text)
        # the table row now displays her new description
        dataset_rows = b.find_elements_by_css_selector("table tbody tr")
        assert_in('This is my first dataset.', dataset_rows[0].text)
    
    def test_dataset_delete(self):
        # A dataset is created
        dataset = DatasetFactory()
        b = self.browser

        # Rosie goes to the datasets index
        datasets_index_url = self.live_server_url + '/datasets/'
        b.get(datasets_index_url)
        # There's one dataset there
        dataset_trs = b.find_elements_by_css_selector('table tbody tr')
        assert_equal(len(dataset_trs), 1)

        # she clicks the delete icon
        delete_icon = b.find_element_by_css_selector('a i.icon-remove')
        delete_icon.click()
        time.sleep(0.5) # NOTE: wait for modal to show up (couldn't get Selenium's wait to work)

        # and a modal confirm dialog appears
        modal_confirm_delete = self.wait.until(lambda d: d.find_element_by_css_selector('.modal-footer a.btn'))
        modal = b.find_element_by_css_selector('.modal')
        assert_in('Delete', modal_confirm_delete.text)
        # There's a warning
        assert_in('WARNING: This operation is irreversible.', modal.text)

        # She confirms
        delete_btn = b.find_element_by_link_text('Delete')
        delete_btn.click()

        # Her dataset is now gone
        dataset_rows = b.find_elements_by_css_selector("table tbody tr")
        assert_equal(len(dataset_rows), 0)


def body_text(browser):
    return browser.find_element_by_tag_name('body').text

def click_submit(browser):
    return browser.find_element_by_css_selector('input.btn[value="Submit"]').click()

def clickable(element):
    if element.is_clickable():
        return element
    return null





       
        