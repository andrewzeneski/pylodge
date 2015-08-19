PyLodge
=======

PyLodge is a framework that integrates the automated tests with TestLodge. It will update the status of the test cases
in TestLodge based on the execution status of the automation script. In case of Failed test cases, it will create a
defect in the issue tracker if the project in TestLodge has the issue tracker configured.


https://github.com/gettalent/pylodge

C

Installation:
=============

To install pylodge, simply:

.. code-block:: bash

    $ pip install pylodge


Recommended Folder Structure for tests:
=======================================

The following example assumes the test automation project directory structure as mentioned below and using py.test

myproject/

pages/
        page1.py

        page2.py

        ...

tests/
        \__init__.py

        conftest.py

        module1/

            test_testcase1.py

        module2/

            test_testcase2.py

             ...


Usage:
======

If you are using the pytest framework, you need to add the following lines of code in the __init__.py file.

This will create a test run in TestLodge whenever your automated tests run::

    from pylodge.pylodge import PyLodge
    pylodge_obj = PyLodge(testlodge_username, testlodge_password, testlodge_project, testlodge_api_url)
    pylodge_obj.create_test_run()

In the conftest.py, you need to write a hook that will read the execution status of your pytest and pass that status to
 pylodge. Something like this::


    @pytest.mark.tryfirst
    def pytest_runtest_makereport( __multicall__):
        rep = __multicall__.execute()
        if rep.when == 'call':
            nodeid = rep.nodeid
            callerlist = nodeid.split("::")
            test_name= os.path.splitext(callerlist[0])[0]
            substring = re.search('test_(.*)', test_name)
            if substring:
                test_name = substring.group(1)
            if rep.passed:
                print 'Passed'
                pylodge_obj.mark_test_as_passed(test_name)
            elif rep.failed:
                print 'Failed'
                pylodge_obj.mark_test_as_failed(test_name)
            elif rep.skipped:
                print 'Skipped'
                pylodge_obj.mark_test_as_skipped(test_name)
        return rep

