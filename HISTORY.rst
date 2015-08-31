.. :changelog:

Release History
---------------

0.2.0 (2015-08-31)
++++++++++++++++++

**Features and Improvements**
pylodge will now create a test run based on user supplied value. If none, it will create a test run with a default time
stamped name

0.1.9 (2015-08-19)
++++++++++++++++++
**Bugfixes**
Bugfix for Minor issue in case-insensitive search

0.1.8 (2015-08-19)
++++++++++++++++++

**Features and Improvements**
pylodge will now do a case-insenitive search in testlodge to find the test name and mark the execution result. This
means that the test name need not be a case sensitive match to the test case name in Test Lodge

0.1.7 (2015-08-18)
++++++++++++++++++

**Features and Improvements**
Major Changes in the implementation. Now pylodge no longer gets the test lodge authentication details from the .cfg file
. You can just pass the auth details in the create_test_run() method. This allows the flexibility of using the framework
 when the scripts are executed through CI.
