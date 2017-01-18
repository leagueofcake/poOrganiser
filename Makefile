init:
	pip install -r requirements.txt

test:
# Automatically find test files
# python -m unittest discover

# Manually specify test files
	python -m unittest tests.testPorgWrapper tests.testEvent tests.testUser tests.testAttendance tests.testChoice tests.testResponse
