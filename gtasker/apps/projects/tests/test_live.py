# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from ...profiles.models import TaskerUser
from ..models import Project


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class ProjectsLiveTestCase(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)
        self.user = TaskerUser.objects.create_user(
            email='foo@bar.bz',
            first_name='foo',
            last_name='bar',
            password='boo'
        )
        TaskerUser.objects.create_user(
            email='boo@bar.bz',
            first_name='boo',
            last_name='bar',
            password='xxx'
        )

        self.url = reverse('projects:main')
        self.browser.get(self.live_server_url + self.url)

    def test_projects_main_view(self):
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')

        username.send_keys('foo@bar.bz')
        password.send_keys('boo')
        password.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')

        self.assertIn('Projects', body.text)

        add = self.browser.find_element_by_id('add_project')
        add.click()

        modal = self.browser.find_element_by_id('project_modal')

        color = self.browser.find_element_by_class_name('current')
        color.click();

        #5 C3411E;
        select_color = self.browser.find_element_by_id('color_5')
        select_color.click()

        current_color = self.browser.find_element_by_class_name('current')
        self.assertEquals(current_color.get_attribute('style'),
                          'background-color: rgb(195, 65, 30);')
        name = self.browser.find_element_by_id('id_name')
        name.send_keys('foo')
        notes = self.browser.find_element_by_id('id_notes')
        notes.send_keys('bar')
        # TODO: add date
        start_date = self.browser.find_element_by_id('id_start_date')
        followers = self.browser.find_element_by_id('id_followers_autocomplete')
        followers.send_keys('foo')
        follower = self.browser.find_element_by_class_name('item')
        follower.click()
        followers.send_keys('boo')
        follower = self.browser.find_element_by_class_name('item')
        follower.click()
        save = self.browser.find_element_by_id('save_project')
        save.click()
        self.assertEquals(Project.objects.count(), 1)
        project = Project.objects.all()[0]
        self.assertEquals(project.followers.count(), 2)

        self.fail('Finish me')

    def tearDown(self):
        self.browser.close()