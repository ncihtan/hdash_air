"""Slack Connector."""
import datetime
import requests
from airflow.models import Variable
from hdash.util.s3_credentials import S3Credentials


class Slack:
    """Slack Connector."""

    SLACK_WEBHOOK_URL = "SLACK_WEBHOOK_URL"

    def __init__(self):
        """Construct Slack Connector."""
        self.s3_credentials = S3Credentials()
        self.web_hook_url = Variable.get(self.SLACK_WEBHOOK_URL)
        if self.web_hook_url is None:
            raise EnvironmentError(f"{self.SLACK_WEBHOOK_URL} not set.")

    def post_msg(self, success):
        """Post Success or Failure to Slack."""
        json_msg = self.create_blocks(success)
        headers = {"Content-type": "application/json"}
        return requests.post(
            self.web_hook_url, json=json_msg, headers=headers, timeout=300
        )

    def create_blocks(self, success):
        """Create JSON Blocks for Posting to Slack."""
        now = datetime.datetime.now()
        payload = {}
        blocks = []
        payload["blocks"] = blocks
        text = self._create_text_block("plain_text", "HTAN Dashboard")
        block1 = {"type": "header", "text": text}
        blocks.append(block1)

        block2 = {"type": "divider"}
        blocks.append(block2)

        block3 = {"type": "section"}
        blocks.append(block3)
        if success:
            text = self._create_text_block(
                "plain_text", f":white_check_mark: Automatically deployed at {now}."
            )
        else:
            text = self._create_text_block(
                "plain_text", f":scream: Failure occurred at {now}."
            )
        block3["text"] = text

        if success:
            text = self._create_text_block(
                "mrkdwn", f"<{self.s3_credentials.web_site_url}|View Dashboard>", False
            )
            block4 = {"type": "section", "text": text}
            blocks.append(block4)
        return payload

    def _create_text_block(self, text_type, msg, emoji=True):
        if emoji:
            return {"type": text_type, "text": msg, "emoji": True}
        return {"type": text_type, "text": msg}
