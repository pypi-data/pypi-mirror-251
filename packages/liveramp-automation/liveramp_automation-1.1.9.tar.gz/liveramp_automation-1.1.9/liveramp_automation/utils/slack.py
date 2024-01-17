import re
import requests
from requests import Response
from html.parser import HTMLParser
from typing import Optional, Dict, Any, Tuple, List, Sequence
from liveramp_automation.utils.log import Logger


class SlackHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        """Escapes and converts an HTML string to Slack flavored Markdown.
        More about Slack's Markdown Flavor (mrkdwn) can be seen here:
            https://api.slack.com/reference/surfaces/formatting
        """
        super().__init__(*args, **kwargs)
        self.slack_message = ''
        self.ignore_tag = False
        self.line_break = '::LINE::BREAK::'

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Any]]):
        """ Called when the opening of a tag is encountered.

        Args:
            tag: Lowercase name of the HTML tag.  E.G. `br` or `i`.
            attrs: List of tuples with the tuple having the following form:
            (attribute name, value).  E.G. ('href', 'www.example.com').
        """
        if tag in ['i', 'em']:
            self.slack_message += '_'
        elif tag in ['b', 'strong']:
            self.slack_message += '*'
        elif tag == 'strike':
            self.slack_message += '~'
        elif tag in ['br', 'p', 'ul']:
            self.slack_message += self.line_break
        elif tag == 'li':
            self.slack_message += f'{self.line_break}- '
        elif tag == 'code':
            self.slack_message += '`'
        elif tag == 'a':
            href = [x[1] for x in attrs if x[0] == 'href']
            if len(href) > 0:
                self.slack_message += f'<{href[0]}|'
        else:
            self.ignore_tag = True

    def handle_data(self, data: str):
        """Handles the data within a tag.

        Args:
        data: The data/string within the HTML tag.
        """
        if not self.ignore_tag:
            self.slack_message += data \
                .replace('&', '&amp;') \
                .replace('<', '&lt;') \
                .replace('>', '&gt;')

    def handle_endtag(self, tag: str):
        """Called when the closing of a tag is encountered. 
        
        Args:
            tag: Lowercase name of the HTML tag.  E.G. `br` or `i`.
        """
        if tag in ['i', 'em']:
            self.slack_message += '_'
        elif tag in ['b', 'strong']:
            self.slack_message += '*'
        elif tag == 'strike':
            self.slack_message += '~'
        elif tag == 'p':
            self.slack_message += self.line_break
        elif tag == 'code':
            self.slack_message += '`'
        elif tag == 'a':
            self.slack_message += '>'

        self.ignore_tag = False

    def parse(self, html_string: str) -> str:
        """Parses a given HTML string and applies simple formatting.

        Args:
        html_string: The HTML string to convert to Slack mrkdwn.

        Returns:
            A formatted Slack mrkdwn string.
        """
        self.feed(html_string)
        return re.sub(
            r'^(\n)+',  # Remove the leading line breaks
            '',
            ' '.join(self.slack_message.split()).replace(self.line_break, '\n')
        )


class WebhookResponse:
    def __init__(
            self,
            *,
            status_code: int,
            body: str,
    ):
        self.status_code = status_code
        self.body = body


class SlackClient:
    def __init__(self,
                 url: str,
                 timeout: Optional[int] = 15,
                 headers: Optional[Dict[str, str]] = None
                 ):
        """ Class to send messages to a provided Slack webhook URL.
        You can read more about Slack's Incoming Webhooks here:
        https://api.slack.com/messaging/webhooks

        Args:
            url: The webhook URL to send a message to.
            timeout: Number of seconds before the request will time out.
            headers: Request headers to append only for this request
        """
        self.url = url
        self.headers = headers if headers else {"Content-Type": "application/json;charset=utf-8", }
        self.timeout = timeout

    def send(self, *,
             message: str,
             attachments: Optional[Sequence[Dict[str, Any]]] = None,
             blocks: Optional[Sequence[Dict[str, Any]]] = None,
             ) -> WebhookResponse:
        """Sends a message to the webhook URL.

        Args:
            message: Plain text string to send to Slack.
            attachments: A collection of attachments
            blocks: A collection of Block Kit UI components

        Returns:
            Webhook response
        """
        payload = {
            'text': message,
            "attachments": attachments,
            "blocks": blocks,
        }
        Logger.debug(f"Sending a request - url: {self.url}, payload: {payload}, headers: {self.headers}")

        http_resp: Optional[Response] = None
        try:
            http_resp = requests.post(self.url,
                                      headers=self.headers,
                                      json=payload,
                                      timeout=self.timeout
                                      )
        except requests.Timeout:
            Logger.error('Timeout occurred when trying to send message to Slack.')
        except requests.RequestException as e:
            Logger.error(f'Error occurred when communicating with Slack: {e}.')
        else:
            Logger.info('Successfully sent message to Slack.')

        response_body: str = http_resp.text
        resp = WebhookResponse(
            status_code=http_resp.status_code,
            body=response_body,
        )
        return resp
