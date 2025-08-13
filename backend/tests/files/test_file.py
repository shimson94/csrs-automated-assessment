import unittest
import tmp_submission

class TestStudentCode(unittest.TestCase):

    def test_add_function(self):
        """Test the 'add_function' for correct addition."""
        self.assertEqual(add_function(2, 3), 5)
        
        self.assertEqual(add_function(-2, -3), -5)
        
        self.assertEqual(add_function(2, -3), -1)
        
        self.assertEqual(add_function(0, 5), 5)
        self.assertEqual(add_function(0, -5), -5)

    def test_factorial(self):
        """Test the 'factorial' function with correct values."""
        self.assertEqual(factorial(5), 120)
        
        self.assertEqual(factorial(0), 1)
        
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_factorial_infinite_loop(self):
        """Test the 'factorial' function to ensure it doesn't run into an infinite loop."""
        
        with self.assertRaises(RecursionError):
            factorial(0)


if __name__ == '__main__':
    unittest.main()