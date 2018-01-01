import argparse
import os
import tempfile
import unittest

from cliez import parser


class CreateTests(unittest.TestCase):
    def setUp(self):
        from cliez import main
        _ = main
        pass

    def test_missing(self):
        """
        missing argument
        :return:
        """

        with self.assertRaises(SystemExit) as cm:
            parser.parse(argparse.ArgumentParser(), argv=['command', 'create'])

        self.assertEqual(2, cm.exception.code)
        pass

    def test_github_mode(self):
        """
        github mode

        .. note::

            you must be specify `--dir` option in testcase


        :return:
        """

        with tempfile.TemporaryDirectory() as dp:
            parser.parse(argparse.ArgumentParser(),
                         argv=['command', 'create',
                               'wangwenpei/cliez-kickstart',
                               '--dir', dp,
                               '--debug'])
            self.assertEqual(True, os.path.exists(
                os.path.join(dp, '.git')
            ))
        pass

    def test_bitbucket_mode(self):
        """
        butbucket mode

        .. note::

            you must be specify `--dir` option in testcase


        :return:
        """

        with tempfile.TemporaryDirectory() as dp:
            parser.parse(argparse.ArgumentParser(),
                         argv=['command', 'create',
                               'nextoa/cliez-kickstart',
                               '--dir', dp,
                               '--bitbucket',
                               '--debug'])
            self.assertEqual(True, os.path.exists(
                os.path.join(dp, '.hg')
            ))
        pass

    def test_final_in_bitbucket(self):
        """
        search github first,
        if not exists,search bitbucket.

        .. note::

            you must be specify `--dir` option in testcase


        :return:
        """
        with tempfile.TemporaryDirectory() as dp:
            parser.parse(argparse.ArgumentParser(),
                         argv=['command', 'create',
                               'nextoa/cliez-kickstart',
                               '--dir', dp,
                               '--debug'])
            self.assertEqual(True, os.path.exists(
                os.path.join(dp, '.hg')
            ))
        pass

    pass


if __name__ == '__main__':
    unittest.main()
