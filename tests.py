from unittest import TestCase
from cliez.loader import ArgLoader


class NormalTest(TestCase):
    def setUp(self):
        self.useage = (
            "Useage  COMMAND [options]  arguments",
            "",
            "document line1",
            "document line2",
            "",  # blank line
            "Options:",
            ("--opt1", "comment for opt", '-a'),
            ("--opt2:", "comment for opt", '-b'),
            "Actions",
            ("@hello", "call hello"),
            "",
            ("--help", "print help document", '-h'),
            ("--debug", "debug mode"),
        )

    pass

    def test_options(self):
        a = ArgLoader(self.useage, ['COMMAND', '-a', '1', '-b', '10'])

        self.assertEqual(True, a.options['--opt1'])
        self.assertEqual('10', a.options['--opt2'])
        self.assertEqual('1', a.argv[1])

        pass

    def test_actions(self):

        a = ArgLoader(self.useage, ['COMMAND', 'hello', '1', '-b', '10'])

        self.assertEqual(True, a.actions['hello'])
        self.assertEqual('10', a.options['--opt2'])
        self.assertEqual('1', a.argv[1])

        pass

    def test_args(self):
        pass

    pass
