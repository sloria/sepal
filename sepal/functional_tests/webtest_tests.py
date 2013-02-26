import os
from glob import glob
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.conf import settings
from nose.tools import *

from sepal.base.tests.factories import UserFactory
from sepal.datasets.tests.factories import *
from sepal.datasets.models import *


class TestAUser(WebTest):

    def setUp(self):
        self.user = UserFactory()
        self.valid_file_name = 'test-valid-file-0821x1.wav'
        self.invalid_file_name = 'test-invalid-txt-file.txt'
        self._login()

    def _login(self):
        # Rosie logs in
        res = self.app.get('/')
        form = res.forms['loginForm']
        form['username'] = self.user.username
        form['password'] = self.user.password
        res = form.submit()
        return res


    def tearDown(self):
        try:
            # Delete all the files uploaded in the tests
            tmp_files = glob(os.path.join(settings.MEDIA_ROOT,
                                 'audio',  
                                 '{}*.wav'.format(self.valid_file_name.split('.')[0])))
            for f in tmp_files:
                os.remove(f)
        except:
            pass

    def test_can_see_the_index(self):
        # Rosie goes to the homepage
        root = self.app.get('/' , user=self.user)

        print self.user.is_authenticated()
        # She clicks on the Datasets link
        res = root.click('Datasets')

        # She sees that there are no datasets
        assert_in('No datasets', res)

        # After a dataset is created
        dataset = DatasetFactory(user=self.user)
        # and clicking the Datasets link again
        res = res.click('Datasets')
        # She sees the new dataset
        print res
        res.mustcontain(dataset.name, dataset.species,
                        dataset.description)

    def test_can_create_a_dataset(self):
        # Rosie goes to the datasets index page
        index = self.app.get(reverse('datasets:index'),
                                user=self.user)
        # She clicks the create link
        res = index.click('Create Dataset')

        form = res.forms['datasetForm']
        # She fills in the species field but NOT the name field
        form['species'] = 'P. californicus'
        res = form.submit('submit')
        # She sees an error
        assert_in("This field is required", res)

        # She fills in a name
        form['name'] = "Rosie's dataset"
        res = form.submit('submit')
        assert_equal(len(Dataset.objects.all()), 1)

        # back at the index page
        res = res.follow()
        assert_equal(reverse('datasets:index'), res.request.path)
        # she sees her new dataset
        res.mustcontain("Rosie&#39;s dataset", "P. californicus")

    def test_can_edit_a_dataset(self):
        # a dataset without a description is created
        dataset = DatasetFactory(description=None, user=self.user)
        # Rosie goes to the dataset edit page
        edit = self.app.get(reverse('datasets:edit', args=(dataset.pk,)), 
                            user=self.user)
        assert_in('Edit Dataset', edit)
        form = edit.forms['datasetEditForm']
        # She enters a description
        form['description'] = 'This is my first dataset'
        # She also edits the species
        form['species'] = 'rat'
        res = form.submit('submit')
        res = res.follow()

        # back at the index
        assert_equal(reverse('datasets:index'), res.request.path)
        # the new attributes have been saved to the database
        dataset = Dataset.objects.latest()
        assert_equal(dataset.species, 'rat')
        assert_equal(dataset.description, 'This is my first dataset')
        # she can see the edited fields on the page
        res.mustcontain('This is my first dataset', 'rat')

    def test_cannot_upload_an_invalid_filetype(self):
        # Rosie goes to the detail page of a dataset
        detail = self._get_detail_response()

        form = detail.forms['upload-form']
        # She tries to upload a text file
        invalid_file_path = os.path.join(
                                os.path.abspath(os.path.dirname(__file__)),
                                self.invalid_file_name      
                            )
        text_file = file(invalid_file_path).read()
        form['files[]'] = self.invalid_file_name, text_file
        # She submits the form
        res = form.submit('None')
        # There is an acceptFileTypes error
        assert_in('error', res)
        assert_in('acceptFileTypes', res)

    def test_cannot_upload_the_same_file_twice(self):
        # A dataset is created
        dataset = DatasetFactory()
        # Rosie uploads a file
        self._upload_a_valid_file(dataset)
        # Rosie tries to upload the same file
        res = self._upload_a_valid_file(dataset)
        # There's an error message
        assert_in('error', res)
        assert_in('fileAlreadyExists', res)

    def test_cannot_upload_a_very_small_file(self):
        detail = self._get_detail_response()
        form = detail.forms['upload-form']
        # Rosie tries to upload a very small file
        form['files[]'] = 'small-file.wav', 'This file is too small'
        res = form.submit('None')
        # But there's an error
        assert_in('error', res)
        assert_in('minFileSize', res)

    def test_can_upload_a_wav_file(self):
        detail = self._get_detail_response()
        form = detail.forms['upload-form']
        # She uploads a wav file
        valid_file_path = os.path.join(
                            os.path.abspath(os.path.dirname(__file__)),
                            self.valid_file_name
                        ) 
        audio_file = file(valid_file_path).read()
        form['files[]'] = self.valid_file_name, audio_file
        # She submits the upload form
        form.submit('None')
        # a new instance has been created in the database
        assert_equal(len(Instance.objects.all()), 1)
        instance = Instance.objects.latest()
        # it has an Audio instance associated with with it
        assert_equal(instance.audio.audio_file.name, u"audio/{}".format(self.valid_file_name))
        # the instance all feature values
        assert_equal(len(instance.values.all()), len(Feature.objects.all()))


    def test_sees_feature_buttons_on_the_detail_page(self):
        # A dataset is created
        dataset = DatasetFactory()
        # A file has been uploaded to it
        self._upload_a_valid_file(dataset)
        # Rosie goes to the detail page
        detail = self.app.get(reverse('datasets:detail', args=(dataset.pk,)))
        # She sees feature names
        detail.mustcontain('Duration', 'Sample rate', 'ZCR')

    
    def _upload_a_valid_file(self, dataset):
        detail = self.app.get(reverse('datasets:detail', 
                                    args=(dataset.pk,))
                                    )
        form = detail.forms['upload-form']
        # She uploads a wav file
        valid_file_path = os.path.join(
                            os.path.abspath(os.path.dirname(__file__)),
                            self.valid_file_name
                        ) 
        audio_file = file(valid_file_path).read()
        form['files[]'] = self.valid_file_name, audio_file
        # She submits the upload form
        res = form.submit('None')
        return res

    def _get_detail_response(self):
        # A dataset is created
        dataset = DatasetFactory()
        # Rosie goes to the dataset's detail page
        return self.app.get(reverse('datasets:detail', 
                                    args=(dataset.pk,))
                                    )

