#!/bin/sh
# Automatically find test files
#python3 -m unittest discover

# Manually specify test files
python3 -m unittest tests.testEvent tests.testUser tests.testEventUser tests.testQuestionChoice
