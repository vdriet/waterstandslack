""" Ophalen van de waterstand bij Zwolle en posten op slack """
import os
import json
from urllib.request import urlopen, Request
from datetime import datetime
from datetime import timedelta
from slacker import Slacker

BASEURL = 'https://waterinfo.rws.nl/api/chart/get' + \
          '?mapType=waterhoogte&locationCode={}({})&values=-48,48'

def lees_json(url):
  """ haal JSON van de URL op """
  req = Request(url=url, headers={'Accept': 'application/json'})
  with urlopen(req) as response:
    content_tekst = response.read().decode('utf-8')
    content_json = json.loads(content_tekst)
    return content_json

def lees_waterstand_json(name, abbr):
  """ lees de informatie van bepaalde locatie """
  return lees_json(BASEURL.format(name,abbr))

def bepaal_standen(content_json):
  """ haal de waterstand uit de gegevens """
  laatstetijd_gemeten = content_json['t0']
  gemeten_standen = content_json['series'][0]['data']
  voorspelde_standen = content_json['series'][1]['data']

  for stand in gemeten_standen:
    if stand['dateTime'] == laatstetijd_gemeten:
      hoogtenu = stand['value']

  if laatstetijd_gemeten.endswith('Z'):
    tijdpatroon = '%Y-%m-%dT%H:%M:%SZ'
    deltatijd = 1
  else:
    tijdpatroon = '%Y-%m-%dT%H:%M:%S+02:00'
    deltatijd = 1

  laatstetijd_obj = datetime.strptime(laatstetijd_gemeten, tijdpatroon) \
                  + timedelta(hours = deltatijd)
  weergave_tijd = laatstetijd_obj.strftime('%d-%m %H:%M')
  morgen_obj = laatstetijd_obj + timedelta(days=1)
  morgen_tekst = morgen_obj.strftime(tijdpatroon)

  hoogtemorgen = hoogtenu
  for stand in voorspelde_standen:
    if stand['dateTime'] == morgen_tekst:
      hoogtemorgen = stand['value']
  return [weergave_tijd, hoogtenu, hoogtemorgen]

def post_waterstand(weergave_tijd, hoogtenu, hoogtemorgen):
  """ post de waterstand op slack """
  slack_id = os.environ['SLACK_ID_RASPBOT']
  slack = Slacker(slack_id)

  slack.chat.post_message('#waterstand', f'Stand {weergave_tijd} {hoogtenu}, morgen {hoogtemorgen}')

def checkwaterstand_en_post():
  """ haal de waterstand en zet die op slack als het aan de voorwaarden voldoet """
  weergave_tijd, hoogtenu, hoogtemorgen = haalwaterstand_default()
  meldingmaken = False
  if hoogtenu > 100 or hoogtemorgen > 100:
    meldingmaken = True
  if hoogtemorgen - hoogtenu > 10 or hoogtenu - hoogtemorgen > 10:
    meldingmaken = True
  uurnu = datetime.now().hour
  if uurnu == 12:
    meldingmaken = True
  if meldingmaken:
    post_waterstand(weergave_tijd, hoogtenu, hoogtemorgen)

def haalwaterstand_en_post():
  """ haal de waterstand en post het sowieso """
  weergave_tijd, hoogtenu, hoogtemorgen = haalwaterstand_default()
  post_waterstand(weergave_tijd, hoogtenu, hoogtemorgen)

def haalwaterstand_default():
  """ haal de waterstand van de standaard locatie """
  content_json = lees_waterstand_json('Katerveer', 'KATV')
  return bepaal_standen(content_json)

def haalwaterstand(name, abbr):
  """ haal de waterstand van een locatie """
  content_json = lees_waterstand_json(name, abbr)
  return bepaal_standen(content_json)

def main():
  """ hoofdroutine met standaard verwerking """
  checkwaterstand_en_post()

if __name__ == "__main__":
  main()
