""" Ophalen van de waterstand bij Zwolle en posten op slack """
import json
import os
from datetime import datetime

import requests
import waterstand


def postberichtinwaterstand(bericht: str) -> None:
  """ zet een bericht in slack kanaal waterstand
  :param bericht: het bericht wat gepost moet worden
  :type bericht: str
  :rtype: None
  """
  webhookurl: str = os.environ.get('WATERSTAND_WEBHOOK_URL', '')
  data: str = json.dumps({"text": bericht})
  headers: dict = {'Content-Type': 'application/json'}
  requests.post(url=webhookurl, timeout=10, headers=headers, data=data)


def postwaterstand(weergavetijd: str, hoogtenu: int, hoogtemorgen: int) -> None:
  """ post de waterstand op slack
  :param weergavetijd: de tijd van de waterstand
  :type weergavetijd: str
  :param hoogtenu: de hoogte op dit moment
  :type hoogtenu: int
  :param hoogtemorgen: de hoogte van morgen
  :type hoogtemorgen: int
  :rtype: None
  """
  postberichtinwaterstand(f'Stand {weergavetijd} {hoogtenu}, morgen {hoogtemorgen}')


def toonlaatstebericht() -> None:
  """ haal de laatste post van de waterstand op
  :rtype: None
  """
  conversationlisturl: str = 'https://slack.com/api/conversations.list'
  token: str = os.environ.get('KOKOSBOT_OAUTH_TOKEN', '')
  headers: dict = {'Authorization': f'Bearer {token}',
                   'Content-Type': 'application/json'}
  with requests.get(url=conversationlisturl,
                    timeout=10,
                    headers=headers) as response:
    convlist: dict = response.json()
  channel: dict
  for channel in convlist.get('channels', {}):
    if channel['name'] == 'waterstand':
      channelid: str = channel['id']
      conversationhistoryurl: str = 'https://slack.com/api/conversations.history'
      data: str = json.dumps({'channel': channelid})
      with requests.post(url=conversationhistoryurl,
                         timeout=10,
                         headers=headers,
                         data=data) as response:
        message: dict = response.json()
      laatste: str = message['messages'][0]['text']
      print(f'Laatste bericht op slack: {laatste}')


def checkwaterstandenpost() -> None:
  """ haal de waterstand en zet die op slack als het aan de voorwaarden voldoet
  :rtype: None
  """
  gegevens: dict = waterstand.haalwaterstand('Katerveer', 'KATV')
  if gegevens['resultaat'] == 'NOK':
    postberichtinwaterstand(gegevens['error'])
  else:
    weergavetijd: str = gegevens['tijd']
    hoogtenu: int = gegevens['nu']
    hoogtemorgen: int = gegevens['morgen']
    meldingmaken: bool = False
    if hoogtenu > 100 or hoogtemorgen > 100:
      meldingmaken = True
    if hoogtemorgen - hoogtenu > 10 or hoogtenu - hoogtemorgen > 10:
      meldingmaken = True
    uurnu: int = datetime.now().hour
    if uurnu == 12:
      meldingmaken = True
    if meldingmaken:
      postwaterstand(weergavetijd, hoogtenu, hoogtemorgen)
  toonlaatstebericht()


def haalwaterstandenpost() -> None:
  """ haal de waterstand en post het sowieso
  :rtype: None
  """
  gegevens: dict = waterstand.haalwaterstand('Katerveer', 'KATV')
  if gegevens['resultaat'] == 'NOK':
    postberichtinwaterstand(gegevens['error'])
  else:
    weergavetijd: str = gegevens['tijd']
    hoogtenu: int = gegevens['nu']
    hoogtemorgen: int = gegevens['morgen']
    postwaterstand(weergavetijd, hoogtenu, hoogtemorgen)


def main() -> None:
  """ hoofdroutine met standaard verwerking """
  checkwaterstandenpost()


if __name__ == "__main__":
  main()
