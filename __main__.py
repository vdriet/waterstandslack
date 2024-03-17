""" Ophalen van de waterstand bij Zwolle en posten op slack """
import os
from datetime import datetime
from slacker import Slacker
from waterstand import haalwaterstand

BASEURL = 'https://waterinfo.rws.nl/api/chart/get' + \
          '?mapType=waterhoogte&locationCode={}({})&values=-48,48'

def postwaterstand(weergavetijd, hoogtenu, hoogtemorgen):
  """ post de waterstand op slack """
  slackid = os.environ['SLACK_ID_RASPBOT']
  slack = Slacker(slackid)

  slack.chat.post_message('#waterstand', f'Stand {weergavetijd} {hoogtenu}, morgen {hoogtemorgen}')

def checkwaterstandenpost():
  """ haal de waterstand en zet die op slack als het aan de voorwaarden voldoet """
  gegevens = haalwaterstand('Katerveer', 'KATV')
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

def haalwaterstandenpost():
  """ haal de waterstand en post het sowieso """
  gegevens = haalwaterstand('Katerveer', 'KATV')
  weergavetijd = gegevens['tijd']
  hoogtenu = gegevens['nu']
  hoogtemorgen = gegevens['morgen']
  postwaterstand(weergavetijd, hoogtenu, hoogtemorgen)

def main():
  """ hoofdroutine met standaard verwerking """
  checkwaterstandenpost()

if __name__ == "__main__":
  main()
