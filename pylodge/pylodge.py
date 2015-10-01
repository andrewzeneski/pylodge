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
        # Get Project ID. This method returns the id of the specified test lodge project .
        response = requests.get(self._api_url + '/v1/projects.json', auth=self._auth_tuple)
        response_dict = response.json()
        self.project_id = filter(lambda project: self._app_name in project.values(), response_dict['projects'])[0]['id']
        return self.project_id

    def create_test_run(self, run_name=None):
        """
        This method will create a test run in Test Lodge including all test suites in it. It will return the run id of
        the created test run.
        :param run_name: If None, will create test run with the timestamped name starting as Automated_Test_Run_
        :return run_id: The test run id
        """

        # Get the Suite IDs of all the suites in the project
        project_id = self.fetch_and_save_project_id()
        response = requests.get(self._api_url + '/v1/projects/%s/suites.json' % project_id,
                                auth=self._auth_tuple)
        response_dict = response.json()

        suite_ids = [suite_dict['id'] for suite_dict in response_dict['suites']]
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S').format()
        if not run_name:
            run_name = 'Automated_Test_Run_' + '-' + time_stamp

        # Create a Test run including all the test suites in the project and get the Test run ID
        response = requests.post(self._api_url + '/v1/projects/%s/runs.json' % project_id,
                                 json={'run': {'name': run_name, 'suite_ids': suite_ids}},
                                 auth=self._auth_tuple)
        response_dict = response.json()
        self.run_id = response_dict['id']
        return self.run_id

    def delete_redundant_test_runs(self,run_name):
        """

        This method will delete any redundant test runs matching the provided test run name except the latest one.
        :param run_name:The name of the Test run which has redundant test runs with the same name.
        :return:
        """
        project_id = self.fetch_and_save_project_id()
        response = requests.get(self._api_url + '/v1/projects/%s/runs.json' % project_id,
                                auth=self._auth_tuple)
        response_dict = response.json()
        test_runs_list = filter(lambda runs: run_name in runs.values(), response_dict['runs'])

        if type(test_runs_list) is list and len(test_runs_list)>1:
            for run in test_runs_list[:-1]:
                run_id=run['id']
                requests.delete(self._api_url + '/v1/projects/%s/runs/%s.json' % (project_id,run_id),
                                auth=self._auth_tuple)



    def update_test_run_name(self,test_run_id, test_run_name):
        """
        This method will update the test run name provided the run id and new the new test run name .
        :param test_run_id:The id of the test run that need to be updated.
        :param test_run_name: The new name of the Test run .
        :return:
        """
        # Updates the test run name
        project_id = self.fetch_and_save_project_id()
        response = requests.get(self._api_url + '/v1/projects/%s/runs/%s.json' % (project_id, test_run_id),
                                 auth=self._auth_tuple)
        response_dict = response.json()
        run_name = response_dict['name']
        test_run_name = run_name + test_run_name
        requests.patch(
            self._api_url + '/v1/projects/%s/runs/%s.json' % (project_id, test_run_id),
            json={
                'run': {'name': test_run_name }},
            auth=self._auth_tuple)

    def fetch_test_run_name(self, test_run_id):
        """
        This method will get the test run name for the provided run id.
        :param test_run_id: The run id  of the Test run that need to be fetched.
        :return: run_name: The test run name
        """
        assert test_run_id, "test_run_id should be set to something"

        # Fetch Test Run Name
        project_id = self.fetch_and_save_project_id()
        response = requests.get(self._api_url + '/v1/projects/%s/runs/%s.json' % (project_id, test_run_id),
                                 auth=self._auth_tuple)
        response_dict = response.json()
        if not response_dict.get('name'):
            raise Exception("fetch_test_run_name: response_dict did not have a name: %s" % str(response_dict))
        run_name = response_dict['name']
        return run_name

    def fetch_test_run_id(self, test_run_name):
        """
        This method will get the test run id for the provided test run name.
        :param test_run_name:The name of the Test run that need to be fetched.
        :return: The test run id
        """

        project_id = self.fetch_and_save_project_id()
        response = requests.get(self._api_url + '/v1/projects/%s/runs.json' % project_id,
                                 auth=self._auth_tuple)
        response_dict = response.json()
        test_runs_id = filter(lambda runs: test_run_name in runs.values(), response_dict['runs'])[0]['id']
        return test_runs_id

    def fetch_and_save_test_case_id_from_test_name(self, test_name=None):
        """
        NOTE:
        TestLodge's test case ID (aka test step ID) is DIFFERENT from the test case NUMBER.

        For example:
        Test case ID: 1234567 (internal to TestLodge, we get it from the API call)
        Test case number: TC-987
        Test case name: test_create_user

        :param test_name: The test case title
        :return test_case_id: The test case id

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
                    return test_case_id



    def fetch_and_save_not_run_test_case_ids(self, test_run_name):
        """
        Gets the test cases not executed in a given test_run_name
         :param test_run_name: The name of test run
         :return A list of test case ids that are not run

        """

        # Make API call to get the test Run ID from the test run name
        project_id = self.fetch_and_save_project_id()
        response = requests.get(self._api_url + '/v1/projects/%s/runs.json' % project_id,
                                 auth=self._auth_tuple)
        response_dict = response.json()
        run_id = filter(lambda runs: test_run_name in runs.values(), response_dict['runs'])[0]['id']
        response = requests.get(self._api_url + '/v1/projects/%s/runs/%s/executed_steps.json' % (project_id, run_id),
                                auth=self._auth_tuple)
        response_dict = response.json()
        pagination_dict = response_dict['pagination']
        total_pages = pagination_dict['total_pages']
        test_case_ids = []

        for page in range(1, total_pages + 1):
            response = requests.get(
                url=self._api_url + '/v1/projects/%s/runs/%s/executed_steps.json' % (project_id, run_id),
                params={'page': page},
                auth=self._auth_tuple)
            response_dict = response.json()
            for executed_steps_dict in response_dict['executed_steps']:
                if executed_steps_dict['passed']==None:
                    test_case_ids.append(executed_steps_dict['id'])
        return test_case_ids

    def mark_test_as_passed(self, test_case_name=None):
        """
        This method will mark the executed step in a test run as Passed in Test Lodge provided the
         executed step title.
        :param test_case_name: The title of the test case
        """
        project_id =self.project_id
        run_id = self.run_id
        test_case_id = self.fetch_and_save_test_case_id_from_test_name(test_case_name)
        requests.patch(
            self._api_url + '/v1/projects/%s/runs/%s/executed_steps/%s.json' % (project_id, run_id, test_case_id),
            json={
                'executed_step': {'actual_result': 'Test Case Passed', 'passed': 1, 'create_issue_tracker_ticket': 0}},
            auth=self._auth_tuple)

    def mark_test_as_passed_runid(self,run_id, test_case_name=None):
        """
        This method will mark the executed step in a test run as Passed in Test Lodge provided the test run id and the executed step title.

        :param test_case_name: The title of the test case for which the status need to be marked in Test Lodge
         run_id: The test run id
        """
        project_id =self.fetch_and_save_project_id()
        test_case_id = self.fetch_and_save_test_case_id_from_test_name_runid(run_id,test_case_name)
        requests.patch(
            self._api_url + '/v1/projects/%s/runs/%s/executed_steps/%s.json' % (project_id, run_id, test_case_id),
            json={
                'executed_step': {'actual_result': 'Test Case Passed', 'passed': 1, 'create_issue_tracker_ticket': 0}},
            auth=self._auth_tuple)

    def mark_test_as_failed(self, test_case_name=None):
        """
        This method will mark the executed step in a test run as Failed in Test Lodge provided the
        executed step title.It will create a issue tracker ticket if the issue tracker is configured for the project.

        :param test_case_name: The title of the test case for which the status need to be marked in Test Lodge
        """
        project_id =self.project_id
        run_id = self.run_id
        test_case_id = self.fetch_and_save_test_case_id_from_test_name(test_case_name)
        requests.patch(
            self._api_url + '/v1/projects/%s/runs/%s/executed_steps/%s.json' % (project_id, run_id, test_case_id),
            json={
                'executed_step': {'actual_result': 'Test Case Failed', 'passed': 0, 'create_issue_tracker_ticket': 1}},
            auth=self._auth_tuple)

    def mark_test_as_failed_runid(self, run_id, test_case_name=None):
        """
        This method will mark the executed step in a test run as Failed in Test Lodge provided the test run id and
        the executed step title. It will create a issue tracker ticket if the issue tracker is configured for the project.

        :param run_id: The run id of the test run which contains the executed step
        test_name: The title of the test case for which the status need to be marked in Test Lodge
        """
        project_id =self.fetch_and_save_project_id()
        test_case_id = self.fetch_and_save_test_case_id_from_test_name_runid(run_id,test_case_name)
        requests.patch(
            self._api_url + '/v1/projects/%s/runs/%s/executed_steps/%s.json' % (project_id, run_id, test_case_id),
            json={
                'executed_step': {'actual_result': 'Test Case Failed', 'passed': 0, 'create_issue_tracker_ticket': 1}},
            auth=self._auth_tuple)

    def mark_test_as_skipped(self, test_case_name=None):
        """
        This method will mark the executed step in a test run as Skipped in Test Lodge provided
        the executed step title.

        :param test_case_name: The title of the test case for which the status need to be marked in Test Lodge
        """
        project_id =self.project_id
        run_id = self.run_id
        test_case_id = self.fetch_and_save_test_case_id_from_test_name(test_case_name)
        requests.patch(
            self._api_url + '/v1/projects/%s/runs/%s/executed_steps/%s.json' % (project_id, run_id, test_case_id),
            json={
                'executed_step': {'actual_result': 'Test Case Skipped', 'passed': 2, 'create_issue_tracker_ticket': 0}},
            auth=self._auth_tuple)

    def mark_test_as_skipped_runid(self, run_id, test_case_name=None):
        """
        This method will mark the executed step in a test run as Skipped in Test Lodge provided
        the executed step title and run id.

        :param test_case_name: The title of the test case for which the status need to be marked in Test Lodge
        run_id: The run id of the test run which contains the executed step
        """
        project_id =self.fetch_and_save_project_id()
        test_case_id = self.fetch_and_save_test_case_id_from_test_name_runid(run_id,test_case_name)
        requests.patch(
            self._api_url + '/v1/projects/%s/runs/%s/executed_steps/%s.json' % (project_id, run_id, test_case_id),
            json={
                'executed_step': {'actual_result': 'Test Case Skipped', 'passed': 2, 'create_issue_tracker_ticket': 0}},
            auth=self._auth_tuple)

    def mark_test_status(self, test_case_name,status='skipped',test_run_name=None,test_log=None):
        """

        This method will mark the executed step in a test run as Passed / Failed / Skipped in Test Lodge
        provided  test run name and the executed step title.
        :param test_case_name: The title of the test case for which the status need to be marked in Test Lodge.
            test_run_name(optional): The run name of the test run which contains the executed step.
            if None, pylodge will assume the created test run as the test run that has the executed test.
            status(optional): The execution status of the test. Passed / Failed / Skipped. The default is Skipped.
            test_log(optional): It is possible to pass a runtime log in to this method.
            If this argument is appropriately set, then pylodge will also insert the runtime log
            as a comment for the executed step
        """
        project_id =self.project_id
        if test_run_name==None:
            run_id = self.run_id
        else:
            run_id = self.fetch_test_run_id(test_run_name)

        test_case_id = self.fetch_and_save_test_case_id_from_test_name(test_case_name)
        if status.lower() == 'passed':
            status_flag = 1
            issue_tracker_flag=0
        elif status.lower() == 'failed':
            status_flag = 0
            issue_tracker_flag=1
        elif status.lower() == 'skipped':
            status_flag = 2
            issue_tracker_flag=0
        requests.patch(
            self._api_url + '/v1/projects/%s/runs/%s/executed_steps/%s.json' % (project_id, run_id, test_case_id),
            json={
                'executed_step': {'actual_result': 'Test Case %s and the log is \n %s'%(status,test_log),
                                  'passed': status_flag, 'create_issue_tracker_ticket': issue_tracker_flag}},
            auth=self._auth_tuple)

    def mark_test_status_multiple(self, test_case_names=None,status='skipped',test_run_name=None, test_case_ids=None):
        """
        This method will mark multiple executed steps in a test run as Passed / Failed / Skipped
        in Test Lodge provided  executed step ids / titles  as  list .
        It will expect either executed step ids or executed step titles as argument.
        If you provide one, the other will become optional.

        :param test_case_names: The list of titles of the test cases for which the status need to be marked in Test Lodge.
                test_case_ids: The list of ids of the test cases for which the status need to be marked in Test Lodge
                test_run_name(optional): The run name of the test run which contains the executed step. if None, pylodge will assume the created test run as the test run that has the executed test.
                status(optional): The execution status of the test. Passed / Failed/ Skipped . The default is Skipped.
        """
        project_id =self.project_id
        if test_run_name==None:
            run_id = self.run_id
        else:
            run_id = self.fetch_test_run_id(test_run_name)

        if test_case_ids==None:
            test_case_ids=[]
            for test_case_name in test_case_names:
                test_case_id = self.fetch_and_save_test_case_id_from_test_name(test_case_name)
                test_case_ids.append(test_case_id)
        for test_case_id in test_case_ids:
            if status.lower() == 'passed':
                status_flag = 1
                issue_tracker_flag=0
            elif status.lower() == 'failed':
                status_flag = 0
                issue_tracker_flag=1
            elif status.lower() == 'skipped':
                status_flag = 2
                issue_tracker_flag=0
            response=requests.patch(self._api_url + '/v1/projects/%s/runs/%s/executed_steps/%s.json'
                                    % (project_id, run_id, test_case_id),
                                    json={'executed_step': {'actual_result': 'Test Case Passed', 'passed': status_flag,
                                                            'create_issue_tracker_ticket': issue_tracker_flag}},
                                    auth=self._auth_tuple)

    def fetch_and_save_test_case_id_from_test_name_runid(self, run_id, test_name=None):
        """
        NOTE:
        TestLodge's test case ID (aka test step ID) is DIFFERENT from the test case NUMBER.

        For example:
        Test case ID: 1234567 (internal to TestLodge, we get it from the API call)
        Test case number: TC-987
        Test case name: test_create_user

        :param test_name: If None, will get it from the stack trace
               run_id: Test Run id

        """


        # Make API call to get the test step ID from the method name
        project_id =self.fetch_and_save_project_id()
        response = requests.get(self._api_url + '/v1/projects/%s/runs/%s/executed_steps.json' % (project_id, run_id),
                                auth=self._auth_tuple)
        response_dict = response.json()
        if not response_dict.get('pagination'):
            raise Exception("mark_test_as_failed_runid: response_dict did not have pagination for Run ID %s: %s"
                            %(run_id, str(response_dict)))

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
                    return test_case_id

        # Set the test step ID
        self.test_case_id = test_case_id
        return self.test_case_id

if __name__ == "__main__":
    pass
