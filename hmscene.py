# encoding: utf-8

import sys
import argparse
from workflow import Workflow, ICON_WARNING, web, PasswordNotFound

basehref = 'https://houmi.herokuapp.com/api/site/'

def main(wf):
  parser = argparse.ArgumentParser()
  parser.add_argument('query', nargs='?', default=None)
  args = parser.parse_args(wf.args)

  try:
    apikey = wf.get_password('apikey')
  except PasswordNotFound:
    wf.add_item('Houm API key not set',
                'Please use hmsetkey to set your Houm API key.',
                valid=False,
                icon=ICON_WARNING)
    wf.send_feedback()
    return 0

  query = args.query

  allItems = None
  if query:
    allItems = wf.filter(query, items(apikey), key=keyForItem)
  else:
    allItems = items(apikey)

  if not allItems:
    wf.add_item('No scenes or lights found', icon=ICON_WARNING)

  for item in allItems:
    name = item['name']
    wf.add_item(title=name,
                subtitle='Activate scene ' + name,
                arg=item['id'],
                valid=True,
                icon='scene.png')

  wf.send_feedback()

def items(apikey):
  conf = siteConfiguration(apikey)
  return map(makeScene, conf['scenes'])

def keyForItem(item):
  return item['name']

def siteConfiguration(apikey):
  return get(apikey)

def get(apikey):
  r = web.get(url(apikey))
  r.raise_for_status()
  return r.json()

def url(apikey):
  return basehref + apikey

def makeScene(json):
  return {'name': json['name'],
          'id': json['_id']}

if __name__ == u"__main__":
  wf = Workflow()
  sys.exit(wf.run(main))
