import unittest
from unittest.mock import patch, MagicMock
from spotlite.task import TaskingManager  # Replace 'task' with the actual name of your Python file if different

class TestTaskingManager(unittest.TestCase):

    def setUp(self):
        self.tasking_manager = TaskingManager(key_id="dummy_id", key_secret="dummy_secret")

    

if __name__ == '__main__':
    unittest.main()
