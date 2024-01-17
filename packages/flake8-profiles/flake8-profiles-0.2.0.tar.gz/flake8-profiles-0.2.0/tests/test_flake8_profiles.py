import os
import subprocess
import unittest


class CommandRunningTestCase(unittest.TestCase):

    env = {}

    def setUp(self):
        env = dict(os.environ)
        env.update(self.env)
        proc = subprocess.Popen(
            ["flake8"] + self.command + ["."],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        stdout, stderr = proc.communicate()
        self.stdout, self.stderr, self.returncode = (
            stdout.decode(), stderr.decode(), proc.returncode,
        )


class NoProfileDirTestCase(CommandRunningTestCase):

    command = []

    def test_no_profile_dir(self):
        self.assertNotEqual(0, self.returncode)
        self.assertIn("No FLAKE8_PROFILE_DIR set", self.stderr)


class NoProfileTestCase(CommandRunningTestCase):

    command = ["--profile", "notfound"]
    env = {"FLAKE8_PROFILE_DIR": "config"}

    def test_no_profile(self):
        self.assertNotEqual(0, self.returncode)
        self.assertIn(
            (
                f"The specified config file does not exist: config{os.sep}"
                "notfound.conf"
            ),
            self.stdout,
        )


class DefaultProfileTestCase(CommandRunningTestCase):

    command = []
    env = {"FLAKE8_PROFILE_DIR": "config"}

    def test_default_profile_from_config(self):
        self.assertIn(
            f"Loaded profile from config{os.sep}default.conf",
            self.stderr,
        )

    def test_default_profile_finds_violations(self):
        self.assertNotEqual(0, self.returncode)
        self.assertIn("D100 Missing docstring in public module", self.stdout)


class ProfileFromCliTestCase(CommandRunningTestCase):

    command = ["--profile", "nodoc"]
    env = {"FLAKE8_PROFILE_DIR": "config"}

    def test_profile_from_cli(self):
        self.assertIn(
            f"Loaded profile from config{os.sep}nodoc.conf",
            self.stderr,
        )

    def test_nodoc_profile_finds_no_violations(self):
        self.assertEqual(0, self.returncode)
        self.assertEqual("", self.stdout)
