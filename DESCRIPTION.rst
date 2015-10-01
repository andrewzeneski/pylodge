PyLodge
=======

PyLodge is a framework that integrates the automated tests with Test Lodge. PyLodge is developed to take advantage of
the rich features of Test Lodge. When  automated scripts are executed, there should always be a way to precisely reflect
 the metrics of the automation scripts . One could either use third party reporting frameworks or
 design their own customized reports to display these metrics.
 But  in most cases, the available framework might not be informative for test management or the user might have to
 spend hours and hours to design a report that reflects these metrics. Test Lodge has rich reporting features that are
 very simple and  informative . PyLodge takes advantage of these features and allows to user to report and track the
 status of the automation scripts in Test Lodge. PyLodge is a tool independent framework.
 It should work with any tool , if it allows reading the test execution status of the script at runtime.
 The user will only have to pass the test execution status to the appropriate pylodge method.
 PyLodge will update the status of the test cases in Test Lodge based on the execution status of the automation script.
  In case of failed test cases, it will create a defect in the issue tracker if the project in Test Lodge has the
  issue tracker configured.
