import os
from unittest.mock import patch

import responses
from freezegun import freeze_time

import waterstandslack

dummywebhook = 'https://hooks.slek.com/dummy'
convlisturl = 'https://slack.com/api/conversations.list'
convhisturl = 'https://slack.com/api/conversations.history'
os.environ['KOKOSBOT_OAUTH_TOKEN'] = 'xoxo-dummy'
os.environ['WATERSTAND_WEBHOOK_URL'] = dummywebhook
listresponse = {'ok': 'true', 'channels': [{'id': 'DUMMYID', 'name': 'waterstand'}]}


@responses.activate
@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'NOK', 'error': 'Foutmelding'})
def test_main_nok_rws(mock_waterstand, capsys):
  responses.add(responses.POST, dummywebhook,
                json={'status': 'ok'}, status=200)
  responses.add(responses.GET, convlisturl,
                json=listresponse, status=200)
  responses.add(responses.POST, convhisturl,
                json={'ok': True, 'messages': [{'subtype': 'bot_message', 'text': 'Gegevens RWS niet beschikbaar'}]},
                status=200)

  waterstandslack.main()

  captured = capsys.readouterr()
  assert mock_waterstand.called is True
  assert captured.out == 'Laatste bericht op slack: Gegevens RWS niet beschikbaar\n'


@responses.activate
@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'NOK', 'error': 'Foutmelding'})
def test_main_nok_waterstand(mock_waterstand, capsys):
  responses.add(responses.POST, dummywebhook,
                json={'status': 'ok'}, status=200)
  responses.add(responses.GET, convlisturl,
                json=listresponse, status=200)
  responses.add(responses.POST, convhisturl,
                json={'ok': True, 'messages': [{'subtype': 'bot_message', 'text': 'Foutmelding'}]}, status=200)

  waterstandslack.main()

  captured = capsys.readouterr()
  assert mock_waterstand.called is True
  assert captured.out == 'Laatste bericht op slack: Foutmelding\n'


@responses.activate
@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 89.0, 'morgen': 97.0})
@freeze_time("2024-12-18 12:05:00")
def test_main_post_at_12(mock_haalwaterstand, capsys):
  responses.add(responses.POST, dummywebhook,
                json={'status': 'ok'}, status=200)
  responses.add(responses.GET, convlisturl,
                json=listresponse, status=200)
  responses.add(responses.POST, convhisturl,
                json={"ok": True, "messages": [{"subtype": "bot_message", "text": "Stand 18-12 11:50 89.0, morgen 97.0",
                                                "ts": "1734519906.082659"}]}, status=200)

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 89.0, morgen 97.0\n'
  assert mock_haalwaterstand.called
  assert len(responses.calls) == 3
  assert responses.calls[0].request.url == dummywebhook


@responses.activate
@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 89.0, 'morgen': 97.0})
@freeze_time("2024-12-18 13:05:00")
def test_main_no_post_at_13(mock_haalwaterstand, capsys):
  responses.add(responses.POST, dummywebhook,
                json={'status': 'ok'}, status=200)
  responses.add(responses.GET, 'https://slack.com/api/conversations.list',
                json=listresponse, status=200)
  responses.add(responses.POST, 'https://slack.com/api/conversations.history',
                json={"ok": True, "messages": [{"subtype": "bot_message", "text": "Stand 18-12 11:50 89.0, morgen 97.0",
                                                "ts": "1734519906.082659"}]}, status=200)

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 89.0, morgen 97.0\n'

  assert mock_haalwaterstand.called
  assert len(responses.calls) == 2


@responses.activate
@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 107.0, 'morgen': 99.0})
@freeze_time("2024-12-18 13:05:00")
def test_main_post_nu_100_plus(mock_haalwaterstand, capsys):
  responses.add(responses.POST, dummywebhook,
                json={'status': 'ok'}, status=200)
  responses.add(responses.GET, 'https://slack.com/api/conversations.list',
                json=listresponse, status=200)
  responses.add(responses.POST, 'https://slack.com/api/conversations.history',
                json={"ok": True, "messages": [
                  {"subtype": "bot_message", "text": "Stand 18-12 11:50 107.0, morgen 99.0",
                   "ts": "1734519906.082659"}]}, status=200)

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 107.0, morgen 99.0\n'

  assert mock_haalwaterstand.called
  assert len(responses.calls) == 3


@responses.activate
@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 99.0, 'morgen': 107.0})
@freeze_time("2024-12-18 13:05:00")
def test_main_post_morgen_100_plus(mock_haalwaterstand, capsys):
  responses.add(responses.POST, dummywebhook,
                json={'status': 'ok'}, status=200)
  responses.add(responses.GET, 'https://slack.com/api/conversations.list',
                json=listresponse, status=200)
  responses.add(responses.POST, 'https://slack.com/api/conversations.history',
                json={"ok": True, "messages": [
                  {"subtype": "bot_message", "text": "Stand 18-12 11:50 99.0, morgen 107.0",
                   "ts": "1734519906.082659"}]}, status=200)

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 99.0, morgen 107.0\n'

  assert mock_haalwaterstand.called
  assert len(responses.calls) == 3


@responses.activate
@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 33.0, 'morgen': 44.0})
@freeze_time("2024-12-18 13:05:00")
def test_main_post_stijging_10_plus(mock_haalwaterstand, capsys):
  responses.add(responses.POST, dummywebhook,
                json={'status': 'ok'}, status=200)
  responses.add(responses.GET, 'https://slack.com/api/conversations.list',
                json=listresponse, status=200)
  responses.add(responses.POST, 'https://slack.com/api/conversations.history',
                json={"ok": True, "messages": [{"subtype": "bot_message", "text": "Stand 18-12 11:50 33.0, morgen 44.0",
                                                "ts": "1734519906.082659"}]}, status=200)

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 33.0, morgen 44.0\n'

  assert mock_haalwaterstand.called
  assert len(responses.calls) == 3


@responses.activate
@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 44.0, 'morgen': 33.0})
@freeze_time("2024-12-18 13:05:00")
def test_main_post_daling_10_plus(mock_haalwaterstand, capsys):
  responses.add(responses.POST, dummywebhook, status=200)
  responses.add(responses.GET, 'https://slack.com/api/conversations.list',
                json=listresponse, status=200)
  responses.add(responses.POST, 'https://slack.com/api/conversations.history',
                json={"ok": True, "messages": [{"subtype": "bot_message", "text": "Stand 18-12 11:50 44.0, morgen 33.0",
                                                "ts": "1734519906.082659"}]}, status=200)

  waterstandslack.main()

  captured = capsys.readouterr()
  assert captured.out == 'Laatste bericht op slack: Stand 18-12 11:50 44.0, morgen 33.0\n'

  assert mock_haalwaterstand.called
  assert len(responses.calls) == 3


@responses.activate
@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'OK', 'tijd': '11:50', 'datum': '18-12', 'nu': 44.0, 'morgen': 33.0})
@freeze_time("2024-12-18 13:05:00")
def test_haalwaterstandenpost(mock_haalwaterstand):
  responses.add(responses.POST, dummywebhook,
                json={'status': 'ok'}, status=200)

  waterstandslack.haalwaterstandenpost()

  assert mock_haalwaterstand.called
  assert len(responses.calls) == 1


@responses.activate
@patch('waterstand.haalwaterstand',
       return_value={'resultaat': 'NOK', 'error': 'Foutmelding'})
def test_haalwaterstandenpost_fout(mock_haalwaterstand):
  responses.add(responses.POST, dummywebhook,
                json={'status': 'ok'}, status=200)

  waterstandslack.haalwaterstandenpost()

  assert mock_haalwaterstand.called
  assert len(responses.calls) == 1
