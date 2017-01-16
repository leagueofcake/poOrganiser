init:
	pip install -r requirements.txt

test:
# Automatically find test files
	python -m unittest discover

# Manually specify test files
# python -m unittest tests.testEvent tests.testUser tests.testAttendance tests.testQuestionChoice tests.testQuestion