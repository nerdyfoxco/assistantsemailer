import unittest
import json
import os
import validate_drc
from unittest.mock import patch, mock_open

class TestDRC(unittest.TestCase):

    def setUp(self):
        self.valid_json = {
            "contract_version": "1.0",
            "deployment_id": "test_deploy",
            "required_capabilities": [],
            "security_floor": {
                "no_autonomous_send": True,
                "user_final_authority_lock": True
            },
            "exit_condition": {}
        }

    def test_01_script_exists(self):
        """Test existence of validator."""
        self.assertTrue(os.path.exists("validate_drc.py"))

    def test_02_contract_exists(self):
        """Test existence of contract file."""
        self.assertTrue(os.path.exists("deployment_readiness.json"))

    def test_03_valid_json_passes(self):
        """Test that valid JSON passes validation."""
        with patch("builtins.open", mock_open(read_data=json.dumps(self.valid_json))):
            with patch("os.path.exists", return_value=True):
                self.assertTrue(validate_drc.validate_drc("dummy.json"))

    def test_04_missing_keys_fail(self):
        """Test missing required keys."""
        invalid = self.valid_json.copy()
        del invalid["deployment_id"]
        with patch("builtins.open", mock_open(read_data=json.dumps(invalid))):
            with patch("os.path.exists", return_value=True):
                self.assertFalse(validate_drc.validate_drc("dummy.json"))

    def test_05_security_floor_auto_send(self):
        """Test violation of no_autonomous_send."""
        invalid = self.valid_json.copy()
        invalid["security_floor"]["no_autonomous_send"] = False
        with patch("builtins.open", mock_open(read_data=json.dumps(invalid))):
            with patch("os.path.exists", return_value=True):
                self.assertFalse(validate_drc.validate_drc("dummy.json"))

    def test_06_authority_lock(self):
        """Test violation of user_final_authority_lock."""
        invalid = self.valid_json.copy()
        invalid["security_floor"]["user_final_authority_lock"] = False
        with patch("builtins.open", mock_open(read_data=json.dumps(invalid))):
            with patch("os.path.exists", return_value=True):
                self.assertFalse(validate_drc.validate_drc("dummy.json"))

    def test_07_malformed_json(self):
        """Test handling of invalid JSON syntax."""
        with patch("builtins.open", mock_open(read_data="{ bad json ")):
            with patch("os.path.exists", return_value=True):
                self.assertFalse(validate_drc.validate_drc("dummy.json"))

    def test_08_file_not_found(self):
        """Test file missing."""
        with patch("os.path.exists", return_value=False):
            self.assertFalse(validate_drc.validate_drc("missing.json"))

    def test_09_integration_real_file(self):
        """Test the ACTUAL deployment_readiness.json file on disk."""
        self.assertTrue(validate_drc.validate_drc("deployment_readiness.json"))

    def test_10_version_check(self):
        """Test that version is a string."""
        with open("deployment_readiness.json", "r") as f:
            data = json.load(f)
        self.assertIsInstance(data["contract_version"], str)

if __name__ == '__main__':
    unittest.main()
