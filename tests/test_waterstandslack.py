import os
from unittest.mock import patch, Mock

from freezegun import freeze_time

import waterstandslack

listresponse = Mock()
listresponse.body = {'ok': 'true', 'channels': [{'id': 'DUMMYID', 'name': 'waterstand'}]}

histresponsenok = Mock()
histresponsenok.body = {'ok': True, 'messages': [
  {'subtype': 'bot_message', 'text': 'Gegevens RWS niet beschikbaar'}]}


@patch('waterstand.haalwaterstand', return_value={'resultaat': 'NOK'})
@patch('slacker.Chat.post_message', return_value=None)
@patch('slacker.Conversations.list', return_value=listresponse)
@patch('slacker.Conversations.history', return_value=histresponsenok)
def test_main_nok(mock_converstations_history, mock_converstations_list, mock_post_message, mock_haalwaterstand,
                  capsys):
  os.environ['SLACK_ID_RASPBOT'] = 'DUMMY'

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Gegevens RWS niet beschikbaar\n'

  assert mock_haalwaterstand.called
  assert mock_post_message.called
  assert mock_converstations_list.called
  assert mock_converstations_history.called


histresponse = Mock()
histresponse.body = {"ok": True, "messages": [
  {"subtype": "bot_message", "text": "Stand 18-12 11:50 89.0, morgen 97.0", "ts": "1734519906.082659"}]}


@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 89.0, 'morgen': 97.0})
@patch('slacker.Chat.post_message', return_value=None)
@patch('slacker.Conversations.list', return_value=listresponse)
@patch('slacker.Conversations.history', return_value=histresponse)
@freeze_time("2024-12-18 12:05:00")
def test_main_post_at_12(mock_converstations_history, mock_converstations_list, mock_post_message,
                         mock_haalwaterstand, capsys):
  os.environ['SLACK_ID_RASPBOT'] = 'DUMMY'

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 89.0, morgen 97.0\n'

  assert mock_haalwaterstand.called
  assert mock_post_message.called
  assert mock_converstations_list.called
  assert mock_converstations_history.called


@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 89.0, 'morgen': 97.0})
@patch('slacker.Chat.post_message', return_value=None)
@patch('slacker.Conversations.list', return_value=listresponse)
@patch('slacker.Conversations.history', return_value=histresponse)
@freeze_time("2024-12-18 13:05:00")
def test_main_no_post_at_13(mock_converstations_history, mock_converstations_list, mock_post_message,
                            mock_haalwaterstand, capsys):
  os.environ['SLACK_ID_RASPBOT'] = 'DUMMY'

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 89.0, morgen 97.0\n'

  assert mock_haalwaterstand.called
  assert not mock_post_message.called
  assert mock_converstations_list.called
  assert mock_converstations_history.called


@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 107.0, 'morgen': 99.0})
@patch('slacker.Chat.post_message', return_value=None)
@patch('slacker.Conversations.list', return_value=listresponse)
@patch('slacker.Conversations.history', return_value=histresponse)
@freeze_time("2024-12-18 13:05:00")
def test_main_post_nu_100_plus(mock_converstations_history, mock_converstations_list, mock_post_message,
                               mock_haalwaterstand, capsys):
  os.environ['SLACK_ID_RASPBOT'] = 'DUMMY'

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 89.0, morgen 97.0\n'

  assert mock_haalwaterstand.called
  assert mock_post_message.called
  assert mock_converstations_list.called
  assert mock_converstations_history.called


@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 99.0, 'morgen': 107.0})
@patch('slacker.Chat.post_message', return_value=None)
@patch('slacker.Conversations.list', return_value=listresponse)
@patch('slacker.Conversations.history', return_value=histresponse)
@freeze_time("2024-12-18 13:05:00")
def test_main_post_morgen_100_plus(mock_converstations_history, mock_converstations_list, mock_post_message,
                                   mock_haalwaterstand, capsys):
  os.environ['SLACK_ID_RASPBOT'] = 'DUMMY'

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 89.0, morgen 97.0\n'

  assert mock_haalwaterstand.called
  assert mock_post_message.called
  assert mock_converstations_list.called
  assert mock_converstations_history.called


@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 33.0, 'morgen': 44.0})
@patch('slacker.Chat.post_message', return_value=None)
@patch('slacker.Conversations.list', return_value=listresponse)
@patch('slacker.Conversations.history', return_value=histresponse)
@freeze_time("2024-12-18 13:05:00")
def test_main_post_stijging_10_plus(mock_converstations_history, mock_converstations_list, mock_post_message,
                                    mock_haalwaterstand, capsys):
  os.environ['SLACK_ID_RASPBOT'] = 'DUMMY'

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 89.0, morgen 97.0\n'

  assert mock_haalwaterstand.called
  assert mock_post_message.called
  assert mock_converstations_list.called
  assert mock_converstations_history.called


@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 44.0, 'morgen': 33.0})
@patch('slacker.Chat.post_message', return_value=None)
@patch('slacker.Conversations.list', return_value=listresponse)
@patch('slacker.Conversations.history', return_value=histresponse)
@freeze_time("2024-12-18 13:05:00")
def test_main_post_daling_10_plus(mock_converstations_history, mock_converstations_list, mock_post_message,
                                  mock_haalwaterstand, capsys):
  os.environ['SLACK_ID_RASPBOT'] = 'DUMMY'

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 89.0, morgen 97.0\n'

  assert mock_haalwaterstand.called
  assert mock_post_message.called
  assert mock_converstations_list.called
  assert mock_converstations_history.called


@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 44.0, 'morgen': 33.0})
@patch('slacker.Chat.post_message', return_value=None)
@freeze_time("2024-12-18 13:05:00")
def test_haalwaterstandenpost(mock_post_message, mock_haalwaterstand):
  os.environ['SLACK_ID_RASPBOT'] = 'DUMMY'

  waterstandslack.haalwaterstandenpost()

  assert mock_haalwaterstand.called
  assert mock_post_message.called

@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'NOK', 'tekst': 'Foutmelding'})
@patch('slacker.Chat.post_message', return_value=None)
@freeze_time("2024-12-18 13:05:00")
def test_haalwaterstandenpost_fout(mock_post_message, mock_haalwaterstand):
  os.environ['SLACK_ID_RASPBOT'] = 'DUMMY'

  waterstandslack.haalwaterstandenpost()

  assert mock_haalwaterstand.called
  assert mock_post_message.called
