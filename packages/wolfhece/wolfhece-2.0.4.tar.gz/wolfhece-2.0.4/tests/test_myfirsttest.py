import _add_path
import unittest


class MyFirstTest(unittest.TestCase):

    def test_helloworld(self):

        a = "Hello World !"

        self.assertEqual(a, 'Hello World !', 'Bad chain with case')
        self.assertEqual(a.lower(), 'hello world !', 'Bad chain lower case')
        self.assertEqual(a.upper(), 'HELLO WORLD !', 'Bad chain lower case')

    def firstfunc(a):
        return a+1

    def test_firstfunc(self):
        self.assertEqual(MyFirstTest.firstfunc(3), 4, 'Bad result')