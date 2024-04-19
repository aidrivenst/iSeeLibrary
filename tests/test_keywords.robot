*** Settings ***
Library    ../iSee/imageKeywords.py
Library    AppiumLibrary
Documentation    This file is for testing python functions on top of the RobotFramework
...              pip install -r testenvrequirements.txt
...              use the following command to run test
...              cd tests/ (mandatory to be in this folder before running the next command)
...              browserstack-sdk robot -d results/ test_keywords.robot 
*** Variables ***
${REMOTE_URL}     https://hub-cloud.browserstack.com/wd/hub
*** Test Cases ***
Test Click Image
    [Documentation]
    Open Application    ${REMOTE_URL}
    Capture Page Screenshot