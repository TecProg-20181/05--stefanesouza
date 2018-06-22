import unittest
import subprocess
import diskspace
import os
import sys
import StringIO


class DiskspaceTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_subprocess_check_output(self):
        cmd = 'du -d 1 .'

        subprocess_return = subprocess.check_output(cmd.strip().split(' '))
        diskspace_check_output_return = diskspace.subprocess_check_output(cmd)

        self.assertEqual(subprocess_return, diskspace_check_output_return)

    def test_bytes_to_readable_with_zero(self):
        blocks = 0
        number_of_bytes = diskspace.bytes_to_readable(blocks)

        self.assertEqual(number_of_bytes, '0.00B')

    def test_bytes_to_readable_with_one(self):
        blocks = 1
        number_of_bytes = diskspace.bytes_to_readable(blocks)

        self.assertEqual(number_of_bytes, '512.00B')

    def test_bytes_to_readable_mb(self):
        blocks = 1000000
        number_of_bytes = diskspace.bytes_to_readable(blocks)

        self.assertEqual(number_of_bytes, '488.28Mb')

    def test_bytes_to_readable_gb(self):
        blocks = 2097152
        number_of_bytes = diskspace.bytes_to_readable(blocks)

        self.assertEqual(number_of_bytes, '1.00Gb')

    def test_bytes_to_readable_tb(self):
        blocks = 2871947673
        number_of_bytes = diskspace.bytes_to_readable(blocks)

        self.assertEqual(number_of_bytes, '1.34Tb')

    def test_print_tree(self):
        file_tree = {}

        file_tree_node = {
            'print_size': '2.00Kb',
            'children': [
                '/home/folder1'
            ],
            'size': 4
        }

        file_tree = {
            '/home': {
                'print_size': '24.00Kb',
                'children': [
                    '/home/folder1'
                ],
                'size': 48
            },
            "/home/folder1": {
                'print_size': '1.00Kb',
                'children': [],
                'size': 2
            }
        }

        path = '/home'

        largest_size = 7

        total_size = 48

        captured_output = StringIO.StringIO()
        sys.stdout = captured_output

        result = ' 2.00Kb    8%  /home\n 1.00Kb    4%  /home/folder1\n'

        diskspace.print_tree(
            file_tree,
            file_tree_node,
            path,
            largest_size,
            total_size)

        sys.stdout = sys.__stdout__

        self.assertEqual(result, captured_output.getvalue())
