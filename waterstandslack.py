""" Ophalen van de waterstand bij Zwolle en posten op slack """
import os
from datetime import datetime
from slacker import Slacker
import waterstand


def postberichtinwaterstand(bericht):
  """ zet een bericht in slack kanaal waterstand """
  slackid = os.environ['SLACK_ID_RASPBOT']
  slack = Slacker(slackid)

  slack.chat.post_message('#waterstand', bericht)


def postwaterstand(weergavetijd, hoogtenu, hoogtemorgen):
  """ post de waterstand op slack """
  postberichtinwaterstand(f'Stand {weergavetijd} {hoogtenu}, morgen {hoogtemorgen}')


def toonlaatstebericht():
  """ haal de laatste post van de waterstand op """
  slackid = os.environ['SLACK_ID_RASPBOT']
  slack = Slacker(slackid)
  convlist = slack.conversations.list()
  for channel in convlist.body['channels']:
    if channel['name'] == 'waterstand':
      channelid = channel['id']
      message = slack.conversations.history(channel=channelid, limit=1)
      laatste = message.body['messages'][0]['text']
      print(f'Laatste bericht op slack: {laatste}')


def checkwaterstandenpost():
  """ haal de waterstand en zet die op slack als het aan de voorwaarden voldoet """
  gegevens = waterstand.haalwaterstand('Katerveer', 'KATV')
  if gegevens['resultaat'] == 'NOK':
    postberichtinwaterstand(gegevens)
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


if __name__ == "__main__":  # pragma: no cover
  main()
