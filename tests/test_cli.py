import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from serial.tools.list_ports_common import ListPortInfo

from lss.cli import filter_ports, main


def port(device, description):
    result = ListPortInfo(device)
    result.description = description
    return result


class CliTests(unittest.TestCase):
    def test_filter_matches_device_name_and_description(self):
        usb = port("COM10", "USB Serial")
        other = port("COM2", None)
        self.assertEqual(filter_ports([usb, other], "uSb"), [usb])
        self.assertEqual(filter_ports([usb, other], "com2"), [other])
        usb.name = "custom-name"
        self.assertEqual(filter_ports([usb, other], "CUSTOM"), [usb])
        self.assertEqual(filter_ports([usb, other], ""), [other, usb])

    def test_filter_is_literal(self):
        usb = port("COM3", "USB (Serial)")
        self.assertEqual(filter_ports([usb], "(Serial)"), [usb])
        self.assertEqual(filter_ports([usb], ".*"), [])

    def test_cli_filter_forms_and_output(self):
        for argv in (["usb"], ["--filter", "usb"], ["-f", "usb"]):
            with self.subTest(argv=argv), patch(
                "lss.cli.list_ports.comports",
                return_value=[port("COM3", "USB Serial"), port("COM2", "Other")],
            ), redirect_stdout(io.StringIO()) as output:
                self.assertEqual(main(argv), 0)
                self.assertIn("DESCRIPTION", output.getvalue())
                self.assertIn("USB Serial", output.getvalue())
                self.assertNotIn("COM2", output.getvalue())

    def test_empty_results(self):
        for argv, message in (([], "No serial ports found."), (["usb"], "No matching serial ports.")):
            with patch("lss.cli.list_ports.comports", return_value=[]), redirect_stdout(io.StringIO()) as output:
                self.assertEqual(main(argv), 0)
                self.assertEqual(output.getvalue().strip(), message)

    def test_discovery_error(self):
        with patch("lss.cli.list_ports.comports", side_effect=OSError("unavailable")), redirect_stderr(io.StringIO()) as output:
            self.assertEqual(main([]), 1)
            self.assertIn("unavailable", output.getvalue())

    def test_conflicting_arguments(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            main(["usb", "--filter", "com"])
        self.assertEqual(raised.exception.code, 2)
