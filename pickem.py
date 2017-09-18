#!/usr/bin/env python
import requests
import sys
from lxml import html
from operator import itemgetter
from pprint import pprint

week = sys.argv[1]
game_type = str.lower(sys.argv[2])

if game_type == 'nfl':
    url = 'https://football.fantasysports.yahoo.com/pickem/pickdistribution?gid=&week='
    url += week
    url += '&type=sc'
elif game_type == 'college':
    url = 'https://football.fantasysports.yahoo.com/college/pickdistribution?gid=&week='
    url += week
    url += '&type=sc'
else:
    print 'type "nfl" or "college" as the second argument'
    exit()

page = requests.get(url)
tree = html.fromstring(page.content)

fav_pref_team = tree.xpath('//*[@class="ysf-matchup-dist yspmainmodule"]//*[@class="favorite pick-preferred"]//*[@class="team"]/a//text()')
fav_pref_pct = tree.xpath('//*[@class="ysf-matchup-dist yspmainmodule"]//*[@class="favorite pick-preferred"]//dd[@class="percent"]//text()')
fav_pref_raw_points = tree.xpath('//*[@class="ysf-matchup-dist yspmainmodule"]//*[@class="favorite pick-preferred"]//dd[@class="team"]/text()')
fav_pref_points = list(filter(lambda x: x != '@', [d.strip() for d in fav_pref_raw_points]))
fav_pref_list = zip(fav_pref_team, fav_pref_pct, fav_pref_points)

ud_pref_team = tree.xpath('//*[@class="ysf-matchup-dist yspmainmodule"]//*[@class="underdog pick-preferred"]//*[@class="team"]/a//text()')
ud_pref_pct = tree.xpath('//*[@class="ysf-matchup-dist yspmainmodule"]//*[@class="underdog pick-preferred"]//dd[@class="percent"]//text()')
ud_pref_raw_points = tree.xpath('//*[@class="ysf-matchup-dist yspmainmodule"]//*[@class="underdog pick-preferred"]//dd[@class="team"]/text()')
ud_pref_points = list(filter(lambda x: x != '@', [d.strip() for d in ud_pref_raw_points]))
ud_pref_list = zip(ud_pref_team, ud_pref_pct, ud_pref_points)

pref_list = fav_pref_list + ud_pref_list
pref_list = sorted(pref_list, key=itemgetter(1), reverse=True)

print 'Week', week, '- Football, foootball picks. (gangster voice)'
pprint(pref_list)
