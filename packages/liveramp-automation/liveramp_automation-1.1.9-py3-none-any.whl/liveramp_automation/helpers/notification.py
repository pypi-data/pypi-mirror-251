from typing import Optional, Dict, Any, Sequence
from liveramp_automation.utils.slack import SlackHTMLParser, SlackClient, WebhookResponse


class NotificationHelper:
    @staticmethod
    def slack_notify(*,
                     webhook_url: str,
                     message: str,
                     attachments: Optional[Sequence[Dict[str, Any]]] = None,
                     blocks: Optional[Sequence[Dict[str, Any]]] = None,
                     parsed_html_flag: Optional[bool] = False) -> WebhookResponse:
        """Sends a message to the webhook URL.

        Args:
            message: Plain text string to send to Slack.
            attachments: A collection of attachments
            blocks: A collection of Block Kit UI components
            parsed_html_flag: A flag indicates whether need parse the parameter message, otherwise send the message to Slack directly. default: False 

        Returns:
            Webhook response

        Example:
        WEBHOOk_URL = "https://hooks.slack.com/services/xxxxx/xxxxxx/xxxxxx"
        html_string = '''
            <p>
                Here <i>is</i> a <strike>paragraph</strike> with a <b>lot</b> of formatting.
            </p>
            <br>
            <code>Code sample</code> & testing escape.
            <ul>
                <li>
                    <a href="https://www.google.com">Google</a>
                </li>
                <li>
                    <a href="https://www.amazon.com">Amazon</a>
                </li>
            </ul>
        '''
        blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "New request"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Type:*\nPaid Time Off"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Created by:*\n<example.com|Fred Enriquez>"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*When:*\nAug 10 - Aug 13"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "<https://example.com|View request>"
                    }
                }
            ]

        attachments = [
            {
                "fallback": "Plain-text summary of the attachment.",
                "color": "#2eb886",
                "pretext": "Optional text that appears above the attachment block",
                "author_name": "Bobby Tables",
                "author_link": "http://flickr.com/bobby/",
                "author_icon": "http://flickr.com/icons/bobby.jpg",
                "title": "Slack API Documentation",
                "title_link": "https://api.slack.com/",
                "text": "Optional text that appears within the attachment",
                "fields": [
                    {
                        "title": "Priority",
                        "value": "High",
                        "short": False
                    }
                ],
                "image_url": "http://my-website.com/path/to/image.jpg",
                "thumb_url": "http://example.com/path/to/thumb.png",
                "footer": "Slack API",
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                "ts": 123456789
            }
        ]
        NotificationHelper.slack_notify(webhook_url=WEBHOOk_URL, message="test")
        NotificationHelper.slack_notify(webhook_url=WEBHOOk_URL, message=html_string, parsed_html_flag=True)
        NotificationHelper.slack_notify(webhook_url=WEBHOOk_URL, message="test", attachments=attachments, blocks=blocks)
        :param webhook_url:
        """
        client = SlackClient(url=webhook_url)
        if parsed_html_flag:
            parser = SlackHTMLParser()
            message = parser.parse(message)
        return client.send(message=message, attachments=attachments, blocks=blocks)

    def pagerduty_notify(self):
        return

    def oc_notify(self):
        return
