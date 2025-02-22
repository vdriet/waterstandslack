""" Ophalen van de waterstand bij Zwolle en posten op slack """
import os
from datetime import datetime
import json
import requests
import waterstand


def postberichtinwaterstand(bericht):
  """ zet een bericht in slack kanaal waterstand """
  webhookurl = os.environ['WATERSTAND_WEBHOOK_URL']
  data = json.dumps({"text": bericht})
  headers = {'Content-Type': 'application/json'}
  requests.post(url=webhookurl, timeout=10, headers=headers, data=data)


def postwaterstand(weergavetijd, hoogtenu, hoogtemorgen):
  """ post de waterstand op slack """
  postberichtinwaterstand(f'Stand {weergavetijd} {hoogtenu}, morgen {hoogtemorgen}')


def toonlaatstebericht():
  """ haal de laatste post van de waterstand op """
  conversationlisturl = 'https://slack.com/api/conversations.list'
  token = os.environ['KOKOSBOT_OAUTH_TOKEN']
  headers = {'Authorization': f'Bearer {token}',
             'Content-Type': 'application/json'}
  with requests.get(url=conversationlisturl,
                    timeout=10,
                    headers=headers) as response:
    convlist = response.json()
  for channel in convlist['channels']:
    if channel['name'] == 'waterstand':
      channelid = channel['id']
      conversationhistoryurl = 'https://slack.com/api/conversations.history'
      data=json.dumps({'channel': channelid})
      with requests.post(url=conversationhistoryurl,
                        timeout=10,
                        headers=headers,
                        data=data) as response:
        message = response.json()
      laatste = message['messages'][0]['text']
      print(f'Laatste bericht op slack: {laatste}')


def checkwaterstandenpost():
  """ haal de waterstand en zet die op slack als het aan de voorwaarden voldoet """
  gegevens = waterstand.haalwaterstand('Katerveer', 'KATV')
  if gegevens['resultaat'] == 'NOK':
    postberichtinwaterstand(gegevens['tekst'])
  else:
    weergavetijd = gegevens['tijd']
    hoogtenu = gegevens['nu']
    hoogtemorgen = gegevens['morgen']
    meldingmaken = False
    if hoogtenu > 100 or hoogtemorgen > 100:
      meldingmaken = True
    if hoogtemorgen - hoogtenu > 10 or hoogtenu - hoogtemorgen > 10:
      meldingmaken = True
    uurnu = datetime.now().hour
    if uurnu == 12:
      meldingmaken = True
    if meldingmaken:
      postwaterstand(weergavetijd, hoogtenu, hoogtemorgen)
  toonlaatstebericht()


def haalwaterstandenpost():
  """ haal de waterstand en post het sowieso """
  gegevens = waterstand.haalwaterstand('Katerveer', 'KATV')
  if gegevens['resultaat'] == 'NOK':
    postberichtinwaterstand(gegevens['tekst'])
  else:
    weergavetijd = gegevens['tijd']
    hoogtenu = gegevens['nu']
    hoogtemorgen = gegevens['morgen']
    postwaterstand(weergavetijd, hoogtenu, hoogtemorgen)


def main():
  """ hoofdroutine met standaard verwerking """
  checkwaterstandenpost()


if __name__ == "__main__":
  main()
