"""Test Slack Connector."""

import json
from hdash.util.slack import Slack


def test_slack_connector():
    """Test Slack Connector."""
    slack = Slack()
    blocks = slack.create_blocks(True, "Details")
    success_json = json.dumps(blocks, indent=2)
    assert "HDash Bot" in success_json

    blocks = slack.create_blocks(False, "Details")
    fail_json = json.dumps(blocks, indent=2)
    assert ":scream:" in fail_json
