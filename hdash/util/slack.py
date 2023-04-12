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

    def post_msg(self, success, msg_detail):
        """Post Success or Failure to Slack."""
        json_msg = self.create_blocks(success, msg_detail)
        headers = {"Content-type": "application/json"}
        return requests.post(
            self.web_hook_url, json=json_msg, headers=headers, timeout=300
        )

    def create_blocks(self, success, msg_detail):
        """Create JSON Blocks for Posting to Slack."""
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %I:%M:%S %p")
        payload = {}
        blocks = []

        if success:
            payload["text"] = "Dashboard Build Success"
        else:
            payload["text"] = "Dashboard Build Failed"
        
        payload["blocks"] = blocks
        text = self._create_text_block("plain_text", "HDash Bot")
        block1 = {"type": "header", "text": text}
        blocks.append(block1)

        block2 = {"type": "divider"}
        blocks.append(block2)

        block3 = {"type": "section"}
        blocks.append(block3)
        if success:
            text = self._create_text_block(
                "plain_text",
                f":white_check_mark: Dashboard automatically deployed at {now} (GMT).",
            )
        else:
            text = self._create_text_block(
                "plain_text", f":scream: Dashboard Failure occurred at {now} (GMT)."
            )
        block3["text"] = text

        block4 = {"type": "section"}
        blocks.append(block4)
        text = self._create_text_block("plain_text", msg_detail)
        block4["text"] = text

        if success:
            text = self._create_text_block(
                "mrkdwn", f"<{self.s3_credentials.web_site_url}|View Dashboard>"
            )
            block5 = {"type": "section", "text": text}
            blocks.append(block5)
        return payload

    def _create_text_block(self, text_type, msg):
        if text_type == "plain_text":
            return {"type": text_type, "text": msg, "emoji": True}
        return {"type": text_type, "text": msg}
