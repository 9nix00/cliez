from unittest import TestCase
from cliez.loader import ArgLoader


class NormalTest(TestCase):
    def setUp(self):
        self.usage = (
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
        a = ArgLoader(self.usage, ['COMMAND', '-a', '1', '-b', '10'])

        self.assertEqual(True, a.options['--opt1'])
        self.assertEqual('10', a.options['--opt2'])
        self.assertEqual('1', a.argv[1])

        pass

    def test_actions(self):
        a = ArgLoader(self.usage, ['COMMAND', 'hello', '1', '-b', '10'])

        self.assertEqual(True, a.actions['hello'])
        self.assertEqual('10', a.options['--opt2'])
        self.assertEqual('1', a.argv[1])
        self.assertEqual(str, type(a.argv[1]))
        pass

    def test_args(self):
        a = ArgLoader(self.usage, ['COMMAND', 'arg'])
        self.assertEqual('arg', a.argv[1])
        pass

    def test_parent(self):
        a = ArgLoader(self.usage, ['COMMAND', 'hello', '1', '-b', '10', '-c', '-d', '10'])

        usage = (
            ("--opt3", "comment for opt", '-c'),
            ("--opt4:", "comment for opt", '-d')
        )

        b = ArgLoader(options=usage, sys_argv=a.argv)
        self.assertEqual('10', b.options['--opt4'])

        print(a)

        pass

    pass
