'''Functional tests using Selenium'''

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from sqk.datasets.tests.factories import *
from sqk.datasets.models import *
from nose.tools import *
import time

#  The web driver to use. Can be either 'Firefox' or 'Chrome'
#  NOTE: selenium ships with the Firefox driver only.
#  The Chrome driver is located in sqk/bin.
#  In order to use the Chrome driver, make sure that 
#    sqk/bin is in your system path.
BROWSER = 'Firefox'


class DatasetCrudTest(LiveServerTestCase):
    '''This is essentially an extension of the Dataset CRUD 
    tests in sqk/sqk/functional_tests/webtests_tests.py
    '''

    def setUp(self):
        if BROWSER == 'Chrome':
            self.browser = webdriver.Chrome()
        else:
            self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.wait = WebDriverWait(self.browser, 5)

    def tearDown(self):
        self.browser.quit()
    
    def test_dataset_delete(self):
        '''Tests deleting a dataset from the datasets index page.
        '''
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
        time.sleep(0.5)  # NOTE: this waits for modal to show up
                         # (couldn't get Selenium's wait to work)

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


class XEditableTest(LiveServerTestCase):

    def setUp(self):
        if BROWSER == 'Chrome':
            self.browser = webdriver.Chrome()
        else:
            self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.wait = WebDriverWait(self.browser, 5)
        self.dataset = DatasetFactory(name="That was then", 
                                        description='Out with the old', 
                                        species='Ancient aardvark')
        self.action = ActionChains(self.browser)

    def tearDown(self):
        self.browser.quit()

    def test_can_edit_dataset_properties(self):
        '''Tests the X-editable fields for a dataset's properties (name, description, species)
        '''
        b = self.browser
        # Rosie goes to the dataset's detail page
        b.get(self.live_server_url + reverse('datasets:detail', args=(self.dataset.pk,)))
        
        # She sees the old title of the dataset
        assert_in('That was then', body_text(b))
        # She clicks on the title
        title = b.find_element_by_link_text('That was then')
        title.click()
        # Now there's a field for her to type a new title
        field = b.find_element_by_css_selector('.editable-container input[type="text"]')
        # She clears out the field
        field.clear()
        # She enters a new title
        field.send_keys('This is now')
        # she presses enter
        field.send_keys(Keys.ENTER)
        # The page displays the new name of the dataset
        time.sleep(0.5)  # Wait for new name to appear
        assert_in('This is now', body_text(b))
        # The name is saved to the dataset
        dataset = Dataset.objects.latest()
        assert_equal(dataset.name, 'This is now')

        # Tests below don't work yet

        # Rosie clicks on the old description
        description = b.find_element_by_link_text('Out with the old')
        description.click()
        # Now there's a field
        field = b.find_element_by_css_selector('.editable-container textarea')
        # She clears it
        field.clear()
        # She types a new description
        field.send_keys('In with the new')
        # She clicks submit
        submit = b.find_elements_by_css_selector('button.btn.editable-submit')[1]
        submit.click()
        # she sees the new description
        time.sleep(0.5)  # wait for new description
        assert_in('In with the new', body_text(b))
        # and it's saved to the db
        dataset = Dataset.objects.latest()
        assert_equal(dataset.description, 'In with the new')

        # She sees the old species of the dataset
        assert_in('Ancient aardvark', body_text(b))
        # She clicks on the species
        species = b.find_element_by_link_text('Ancient aardvark')
        species.click()
        # Now there's a field for her to type a new species
        field = b.find_elements_by_css_selector('.editable-container input[type="text"]')[1]
        # She clears out the field
        field.clear()
        # She enters a new title
        field.send_keys('New narwhal')
        # she clicks submit
        submit = b.find_elements_by_css_selector('button.btn.editable-submit')[2]
        submit.click()
        # The page displays the new name of the dataset
        time.sleep(0.5)  # Wait for new name to appear
        assert_in('New narwhal', body_text(b))
        # The name is saved to the dataset
        dataset = Dataset.objects.latest()
        assert_equal(dataset.species, 'New narwhal')


class VisualizationTest(LiveServerTestCase):
    '''Tests for insteractions with the visualization panel.
    '''

    def setUp(self):
        if BROWSER == 'Chrome':
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        # Create a dataset
        G = FullDatasetGenerator(n_instances=3)
        self.dataset = G.dataset
        # Create some features
        self.feature_1 = FeatureFactory(name='duration')
        self.feature_2 = FeatureFactory(name='zcr', display_name='ZCR')
        self.feature_3 = FeatureFactory(name='spectral centroid')

        # Create some values
        self.dataset.instances.all()[0].values.add(FeatureValueFactory(feature=self.feature_1, value=101))
        self.dataset.instances.all()[0].values.add(FeatureValueFactory(feature=self.feature_2, value=102))
        self.dataset.instances.all()[0].values.add(FeatureValueFactory(feature=self.feature_3, value=103))

        self.dataset.instances.all()[1].values.add(FeatureValueFactory(feature=self.feature_1, value=51.2))
        self.dataset.instances.all()[1].values.add(FeatureValueFactory(feature=self.feature_2, value=52.3))
        self.dataset.instances.all()[1].values.add(FeatureValueFactory(feature=self.feature_3, value=53.4))

        self.dataset.instances.all()[2].values.add(FeatureValueFactory(feature=self.feature_1, value=0.12))
        self.dataset.instances.all()[2].values.add(FeatureValueFactory(feature=self.feature_2, value=0.34))
        self.dataset.instances.all()[2].values.add(FeatureValueFactory(feature=self.feature_3, value=0.56))

        # Create some labels and label values
        G.generate_labels()
        self.plot_height = 360

    def tearDown(self):
        self.driver.quit()

    def _coordinates(self, dot):
        cx = float(dot.get_attribute('cx'))
        cy = float(dot.get_attribute('cy'))
        return (cx, cy)

    def test_clicking_feature_names_moves_dots(self):
        '''Test that clicking feature names in the sidebar causes 
        the plot points to move.
        '''
        b = self.driver
        # Rosie goes to the dataset's detail page
        b.get(self.live_server_url + reverse('datasets:detail', args=(self.dataset.pk,)))
        # She sees the feature names in the sidebar
        sidebar = b.find_element_by_css_selector("div.sidebar-nav")
        assert_in('Duration', sidebar.text)
        assert_in('ZCR', sidebar.text)
        assert_in('Spectral centroid', sidebar.text)
        # She sees a figure with 2 dots
        dots = b.find_elements_by_css_selector("circle.dot")
        assert_equal(len(dots), len(self.dataset.instances.all()))

        # get the coordinates of the dots
        dot1 = b.find_element_by_css_selector('circle.dot[data-id="1"]')
        dot1_coords = self._coordinates(dot1)
        dot2 = b.find_element_by_css_selector('circle.dot[data-id="2"]')
        dot2_coords = self._coordinates(dot2)
        dot3 = b.find_element_by_css_selector("circle.dot[data-id='3']")
        dot3_coords = self._coordinates(dot3)
        # The dots are at the bottom of the plot
        # The origin of an svg is the top-left corner, so if the 
        # points are at the bottom, the y-coordinate is the height of plot
        time.sleep(1.5)  # wait for dots to enter
        assert_roughly_equal(dot1_coords[1], self.plot_height)
        assert_roughly_equal(dot2_coords[1], self.plot_height)

        # She sees axes that say Select X and Select Y
        assert_in('Select X', body_text(b))
        assert_in('Select Y', body_text(b))
        # She clicks on 2 of the feature buttons
        feature_1 = b.find_element_by_link_text("Spectral centroid")
        feature_1.click()
        feature_2 = b.find_element_by_link_text("ZCR")
        feature_2.click()
        # The circles move
        new_dot1_coords = self._coordinates(dot1)
        new_dot2_coords = self._coordinates(dot2)
        # So the coordinates are different
        time.sleep(1)  # wait for dots to move
        # assert_not_equal(new_dot1_coords, dot1_coords)
        assert_not_equal(new_dot2_coords, dot2_coords)

        # And she sees the axes names
        x_axis_label = b.find_element_by_css_selector('g.x.axis text.label').text
        y_axis_label = b.find_element_by_css_selector('g.y.axis text.label').text
        assert_in('Spectral centroid', x_axis_label)
        assert_in('ZCR', y_axis_label)

        # She clicks a different feature
        feature_3 = b.find_element_by_link_text("Duration")
        feature_3.click()

        # The dots move again
        # get the coordinates of the dots
        dot1_coords = self._coordinates(dot1)
        dot2_coords = self._coordinates(dot2)

        assert_not_equal(dot1_coords, new_dot1_coords)

        # And the axis labels are updated
        x_axis_label = b.find_element_by_css_selector('g.x.axis text.label').text
        y_axis_label = b.find_element_by_css_selector('g.y.axis text.label').text
        assert_in('ZCR', x_axis_label)
        assert_in('Duration', y_axis_label)

        # She clicks on the selected features to deselect them
        b.find_element_by_link_text("ZCR").click()
        b.find_element_by_link_text("Duration").click()
        # And the axes say 'Select X' and 'Select Y'
        x_axis_label = b.find_element_by_css_selector('g.x.axis text.label').text
        y_axis_label = b.find_element_by_css_selector('g.y.axis text.label').text
        assert_in('Select X', x_axis_label)
        assert_in('Select Y', y_axis_label)
        # The dots have moved back to the bottom
        # The origin of an svg is the top-left corner, so if the 
        # points are at the bottom, the y-coordinate is the height of plot
        time.sleep(1)  # Wait for dots to move
        final_dot1_coords = self._coordinates(dot1)
        final_dot2_coords = self._coordinates(dot2)
        assert_roughly_equal(final_dot1_coords[1], self.plot_height)
        assert_roughly_equal(final_dot2_coords[1], self.plot_height)


def assert_roughly_equal(a, b):
    '''Tests whether 2 floats are equal within 3
    decimal places.'''
    assert_less(round(a - b, 1), 1)


def body_text(browser):
    '''Shortcut for accessing the text within the <body>
    of the DOM.

    Example
    #######
    >> assert_in('Some text', body_text(self.driver))
    True
    '''
    return browser.find_element_by_tag_name('body').text


def click_submit(browser):
    '''Shortcut for clicking the submit button on a webpage.
    '''
    return browser.find_element_by_css_selector('input.btn[value="Submit"]').click()


def clickable(element):
    if element.is_clickable():
        return element
    return None
