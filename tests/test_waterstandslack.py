import os
from unittest.mock import patch, Mock

import waterstandslack

listresponse = Mock()
listresponse.body = {'ok': 'true', 'channels': [{'id': 'DUMMYID', 'name': 'waterstand'}]}

histresponse = Mock()
histresponse.body = {"ok": True, "messages": [
  {"subtype": "bot_message", "text": "Stand 18-12 11:50 66.0, morgen 70.0", "type": "message",
   "ts": "1734519906.082659", "bot_id": "B4QABUJ3D", "blocks": [{"type": "rich_text", "block_id": "1I8IR",
                                                                 "elements": [{"type": "rich_text_section",
                                                                               "elements": [{"type": "text",
                                                                                             "text": "Stand 18-12 11:50 66.0, morgen 70.0"}]}]}]}],
                     "has_more": True, "is_limited": False, "pin_count": 0, "channel_actions_ts": None,
                     "channel_actions_count": 0,
                     "response_metadata": {"next_cursor": "bmV4dF90czoxNzM0NDMzNTA1Njk5MzE5"}}


@patch('waterstand.haalwaterstand', return_value={'resultaat': 'NOK'})
@patch('slacker.Chat.post_message', return_value=None)
@patch('slacker.Conversations.list', return_value=listresponse)
@patch('slacker.Conversations.history', return_value=histresponse)
def test_main(mock_converstations_history, mock_converstations_list, mock_post_message, mock_haalwaterstand,
              capsys):
  os.environ['SLACK_ID_RASPBOT'] = 'DUMMY'

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 66.0, morgen 70.0\n'

  assert mock_haalwaterstand.called
  assert mock_post_message.called
  assert mock_converstations_list.called
  assert mock_converstations_history.called
