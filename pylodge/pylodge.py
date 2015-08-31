# Copyright (c) 2015 Ashwin Kondapalli
#
# See the file license.txt for copying permission.
__author__ = 'ashwin'

import datetime

import requests


class PyLodge():
    def __init__(self, username, password, project_name, api_url):
        self.username = username
        self.password = password
        self._app_name = project_name
        self._api_url = api_url
        self._auth_tuple = (self.username, self.password)

    def fetch_and_save_project_id(self):
        # Get Project ID
        response = requests.get(self._api_url + '/v1/projects.json', auth=self._auth_tuple)
        response_dict = response.json()
        self.project_id = filter(lambda project: self._app_name in project.values(), response_dict['projects'])[0]['id']
        return self.project_id

    def create_test_run(self,run_name=None, user_agent=None):
        """

        :param run_name: If None, will create test run with the timestamped name starting as Automated_Test_Run_
        :param user_agent: If None, will create test run with the timestamped name ending as Default_User_Agent
        """
        if not run_name:
            test_run_name = 'Automated_Test_Run_'

        else:
            test_run_name = run_name
        if not user_agent:
            user_agent = 'Default_User_Agent'
        else:
            user_agent = user_agent

        # Get the Suite IDs of all the suites in the project
        project_id = self.fetch_and_save_project_id()
        response = requests.get(self._api_url + '/v1/projects/%s/suites.json' % project_id,
                                auth=self._auth_tuple)
        response_dict = response.json()

        suite_ids = [suite_dict['id'] for suite_dict in response_dict['suites']]
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S').format()
        test_run_name = test_run_name + '-' + time_stamp + '-'+ user_agent

        # Create a Test run including all the test suites in the project and get the Test run ID
        response = requests.post(self._api_url + '/v1/projects/%s/runs.json' % project_id,
                                 json={'run': {'name': test_run_name, 'suite_ids': suite_ids}},
                                 auth=self._auth_tuple)
        response_dict = response.json()
        self.run_id = response_dict['id']
        return self.run_id


    def fetch_and_save_test_case_id_from_test_name(self, test_name=None):
        """
        NOTE:
        TestLodge's test case ID (aka test step ID) is DIFFERENT from the test case NUMBER.

        For example:
        Test case ID: 1234567 (internal to TestLodge, we get it from the API call)
        Test case number: TC-987
        Test case name: test_create_user

        :param test_name: If None, will get it from the stack trace

        """


        # Make API call to get the test step ID from the method name
        project_id = self.project_id
        run_id = self.run_id
        response = requests.get(self._api_url + '/v1/projects/%s/runs/%s/executed_steps.json' % (project_id, run_id),
                                auth=self._auth_tuple)
        response_dict = response.json()
        pagination_dict = response_dict['pagination']
        total_pages = pagination_dict['total_pages']
        test_case_id = None

        for page in range(1, total_pages + 1):
            response = requests.get(
                url=self._api_url + '/v1/projects/%s/runs/%s/executed_steps.json' % (project_id, run_id),
                params={'page': page},
                auth=self._auth_tuple)
            response_dict = response.json()
            for executed_steps_dict in response_dict['executed_steps']:

                if executed_steps_dict['title'].lower() == test_name.lower():
                    test_case_id = executed_steps_dict['id']

        # Set the test step ID
        self.test_case_id = test_case_id
        return self.test_case_id

    def mark_test_as_passed(self, test_case_name=None):
        """

        :param test_case_name: If None, will try to guess from stack trace
        """
        project_id =self.project_id
        run_id = self.run_id
        test_case_id = self.fetch_and_save_test_case_id_from_test_name(test_case_name)
        requests.patch(
            self._api_url + '/v1/projects/%s/runs/%s/executed_steps/%s.json' % (project_id, run_id, test_case_id),
            json={
                'executed_step': {'actual_result': 'Test Case Passed', 'passed': 1, 'create_issue_tracker_ticket': 0}},
            auth=self._auth_tuple)

    def mark_test_as_failed(self, test_case_name=None):
        """

        :param test_case_name: If None, will try to guess from stack trace
        """
        project_id =self.project_id
        run_id = self.run_id
        test_case_id = self.fetch_and_save_test_case_id_from_test_name(test_case_name)
        requests.patch(
            self._api_url + '/v1/projects/%s/runs/%s/executed_steps/%s.json' % (project_id, run_id, test_case_id),
            json={
                'executed_step': {'actual_result': 'Test Case Failed', 'passed': 0, 'create_issue_tracker_ticket': 1}},
            auth=self._auth_tuple)

    def mark_test_as_skipped(self, test_case_name=None):
        """

        :param test_case_name: If None, will try to guess from stack trace
        """
        project_id =self.project_id
        run_id = self.run_id
        test_case_id = self.fetch_and_save_test_case_id_from_test_name(test_case_name)
        requests.patch(
            self._api_url + '/v1/projects/%s/runs/%s/executed_steps/%s.json' % (project_id, run_id, test_case_id),
            json={
                'executed_step': {'actual_result': 'Test Case Skipped', 'passed': 2, 'create_issue_tracker_ticket': 0}},
            auth=self._auth_tuple)


if __name__ == "__main__":
    pass
