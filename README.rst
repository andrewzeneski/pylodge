Introduction
============

PyLodge is a framework that integrates the automated tests with Test Lodge. PyLodge is developed to take advantage of
the rich features of Test Lodge. When  automated scripts are executed, there should always be a way to precisely
reflect the metrics of the automation scripts . One could either use third party reporting frameworks or design their
own customized reports to display these metrics. But  in most cases, the available framework might not be informative
for test management or the user might have to spend hours and hours to design a report that reflects these metrics.
Test Lodge has rich reporting features that are very simple and  informative . PyLodge takes advantage of these
features and allows to user to report and track the status of the automation scripts in Test Lodge. PyLodge is a tool
independent framework. It should work with any tool , if it allows reading the test execution status of the script at
runtime. The user will only have to pass the test execution status to the appropriate pylodge method. PyLodge will
update the status of the test cases in Test Lodge based on the execution status of the automation script. In case of
failed test cases, it will trigger the creation of a defect in the issue tracker via Test Loge API if the project in
Test Lodge has the issue tracker configured.

Installation
============

To install pillage, type the following command in the command line

.. code-block:: bash

    $ pip install pylodge

Quickstart
==========

The user need to pass 4 basic arguments at the time of instantiating the PyLodge class.
They are the Test Lodge API endpoint URL, Test Lodge project, Test Lodge user name and Test Lodge password.
There are various ways that the user can pass these arguments.
The user can store these values in environment variables and then pass the values at the time of instantiating the
PyLodge class. Once the PyLodge class is instantiated, the user can call any of the following pylodge methods .

**1. fetch_and_save_project_id()**

This method returns the id of the specified test lodge project .

Usage example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'],
                              os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    project_id = pylodge_obj.fetch_and_save_project_id()

**2. create_test_run()**

This method will create a test run in Test Lodge including all test suites in it. It will return the run id of the
created test run.

Arguments:
run_name (optional) : The name of the test run that you want to create in test lodge. if this argument is not passed
pylodge will create a test run in Test Lodge by a default name The default test run name is
\Automated_Test_Run_(Current Timestamp)

Usage example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'],
                                   os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    run_id = pylodge_obj.create_test_run(‘Sample_Test_Run’)

**3. fetch_test_run_name()**

This method will get the test run name for the provided run id.

Arguments:
run_id : The run id  of the Test run that need to be fetched.

Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'], 
                                  os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])
                                  run_id = pylodge_obj. fetch_test_run_name(‘12345’)

**4. fetch_test_run_id()**

This method will get the test run id for the provided test run name.

Arguments:
test_run_name: The name of the Test run that need to be fetched.

Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'],
                                   os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    run_id = pylodge_obj. fetch_test_run_id(‘Sample_Test_Run’)

**5. update_test_run_name()**

This method will update the test run name provided the run id and new the new test run name .

Arguments:
run_id: The id of the test run that need to be updated.
test_run_name: The new name of the Test run .

Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'],
                                   os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    pylodge_obj. update_test_run_name(‘12345’,‘Updated_Test_Run’)

**6. delete_redundant_test_runs()**

This method will delete any redundant test runs matching the provided test run name except the latest one.

Arguments:
test_run_name: The name of the Test run which has redundant test runs with the same name.

Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'], 
                                  os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    pylodge_obj. delete_redundant_test_runs(‘My_Test_Run’)

**7. fetch_and_save_test_case_id_from_test_name()**

This method will fetch the executed step id  of a executed step in a test run if executed step title is provided

Arguments:
test_name: The title of the test case for which the id needs to be fetched


Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'], 
                                  os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    run_id = pylodge_obj.create_test_run(‘Sample_Test_Run’)

    test_case_id = pylodge_obj. fetch_and_save_test_case_id_from_test_name(‘My_Test_Case_Title’)

**8. mark_test_as_passed()**

This method will mark the executed step in a test run as “Passed” in Test Lodge provided the executed step title.

Arguments:
test_name: The title of the test case for which the status need to be marked in Test Lodge

Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'], 
                                  os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    run_id = pylodge_obj.create_test_run(‘Sample_Test_Run’)

    pylodge_obj.mark_test_as_passed(‘My_Test_Case_Title’)

**9. mark_test_as_failed()**

This method will mark the executed step in a test run as “Failed” in Test Lodge provided the executed step title.
It will create a issue tracker ticket if the issue tracker is configured for the project.

Arguments:
test_name: The title of the test case for which the status need to be marked in Test Lodge

Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'], 
                                  os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    run_id = pylodge_obj.create_test_run(‘Sample_Test_Run’)

    pylodge_obj.mark_test_as_failed(‘My_Test_Case_Title’)

**10. mark_test_as_skipped()**

This method will mark the executed step in a test run as “Skipped” in Test Lodge provided the executed step title.

Arguments:
test_name: The title of the test case for which the status need to be marked in Test Lodge

Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'], 
                                  os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    run_id = pylodge_obj.create_test_run(‘Sample_Test_Run’)

    pylodge_obj. mark_test_as_skipped(‘My_Test_Case_Title’)

**11. mark_test_as_passed_runid()**

This method will mark the executed step in a test run as “Passed” in Test Lodge provided the test run id and the
executed step title.

Arguments:
run_id: The run id of the test run which contains the executed step
test_name: The title of the test case for which the status need to be marked in Test Lodge

Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'],
                                   os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    pylodge_obj. mark_test_as_passed_runid(‘12345’,‘My_Test_Case_Title’)

**12. mark_test_as_failed_runid()**

This method will mark the executed step in a test run as “Failed” in Test Lodge provided the test run id and the
executed step title. It will create a issue tracker ticket if the issue tracker is configured for the project.

Arguments:
run_id: The run id of the test run which contains the executed step
test_name: The title of the test case for which the status need to be marked in Test Lodge

Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'], 
                                  os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    pylodge_obj. mark_test_as_failed_runid(‘12345’,‘My_Test_Case_Title’)


**13. mark_test_as_skipped_runid()**

This method will mark the executed step in a test run as “Skipped” in Test Lodge provided the test run id and the
executed step title.

Arguments:
run_id: The run id of the test run which contains the executed step
test_name: The title of the test case for which the status need to be marked in Test Lodge

Usage Example::

        pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'],
                                       os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

        pylodge_obj. mark_test_as_skipped_runid(‘12345’,‘My_Test_Case_Title’)

**14. mark_test_status()**

This method will mark the executed step in a test run as “Passed” / “Failed” / “Skipped” in Test Lodge provided
test run name and the executed step title.

Arguments:
test_case_name: The title of the test case for which the status need to be marked in Test Lodge.
test_run_name(optional): The run name of the test run which contains the executed step.
if None, pylodge will assume the created test run as the test run that has the executed test.
status(optional): The execution status of the test. “Passed” / “Failed” / “Skipped” . The default is ‘Skipped’.
test_log(optional): It is possible to pass a runtime log in to this method. If this argument is appropriately set,
then pylodge will also insert the runtime log as a comment for the executed step


Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'], 
                                  os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])
    pylodge_obj. mark_test_status(test_case_name=‘My_Test_Case_Title’,test_run_name=‘My_Test_Run’,status=‘passed’)

**15. mark_test_status_multiple()**

This method will mark multiple executed steps in a test run as “Passed” / “Failed” / “Skipped” in Test Lodge provided
executed step ids / titles  as  list . It will expect either executed step ids or executed step titles as argument.
If you provide one, the other will become optional.

Arguments:
test_case_names: The list of titles of the test cases for which the status need to be marked in Test Lodge.
test_case_ids: The list of ids of the test cases for which the status need to be marked in Test Lodge
test_run_name(optional): The run name of the test run which contains the executed step.
if None, pylodge will assume the created test run as the test run that has the executed test.
status(optional): The execution status of the test. “Passed” / “Failed” / “Skipped” . The default is ‘Skipped’.


Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'],
                                   os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    pylodge_obj. mark_test_status_multiple(test_case_ids=[‘1000’,’1001’,’1002’],test_run_name=‘My_Test_Run’,status=‘passed’)

**15. fetch_and_save_not_run_test_case_ids()**

This method will fetch all the executed steps in a given test run that are “Not Run” as  a list . it will return all the ids as list

Arguments:
test_run_name: The run name of the test run which contains the not run executed steps. i

Usage Example::

    pylodge_obj = pylodge.PyLodge(os.environ['TESTLODGE_USERNAME'], os.environ['TESTLODGE_PASSWORD'], 
                                  os.environ['TESTLODGE_PROJECT'], os.environ['TESTLODGE_API_URL'])

    pylodge_obj. fetch_and_save_not_run_test_case_ids(test_run_name=‘My_Test_Run’)


Example Implementation with selenium webdriver, pytest, xdist and redis :
=========================================================================

My example assumes the test automation project directory structure as mentioned below and using pytest

myproject/

    pages/

        page1.py
        page2.py
        …
    tests/

        \__init__.py
        conftest.py

        module-1-folder/

        test_functional_test_group1.py

        module-2-folder/

        test_functional_test_group2.py
        …
    updatetestlodge.py

The actual tests are implemented as methods inside the test_functional_test_group1.py files. So each of those methods
will have a prefix as ‘test_’ as a standard pytest naming convention and then followed by the test lodge prefix .
For example if test_tc01_create_user() is the automated test, ‘create_user’ will be the associated manual test case
in test lodge and tc01 will be the prefix of that test case.

For our tests we used pytest and redis. The conftest_.py file for our implementation can be found here conftest_ .
Download and start the redis server before running the tests.

.. _conftest: https://gist.github.com/akondapalli/60165ad869f88d4f00bd#file-conftest-py
 
Once the automated scripts are run, the tests along with the execution status and the logs are saved in to redis keys.
You need to write another python script that will extract these reds keys and update the Test Lodge .
Here_ is the code that should be saved in a .py file and executed after all tests are run.

.. _Here: https://gist.github.com/akondapalli/60165ad869f88d4f00bd#file-updatetestlodge-py

