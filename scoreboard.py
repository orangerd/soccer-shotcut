#!/usr/bin/env python3

import curses
import os
import shutil

from curses import wrapper
from curses.textpad import rectangle

from mako.template import Template

SCORES_DIR='/tmp/soccer'

HOME_LOGO='https://spot70-images.s3.amazonaws.com/clubs/logos/000/000/022/thumb/mvla-logo.png'
HOME_NAME='MVLA'
HOME_COLOR='white'
HOME_BGCOLOR='#123764'

WIDTH=600
HEIGHT=WIDTH // 10

class TeamScore(object):
  def __init__(self, team_name, name_x, name_y=0):
    self.team_name = team_name
    self.name_x = name_x
    self.name_y = name_y

    # Get the mid-point for the length of team name
    self.score_x = (len(self.team_name) // 2)
    # Subtract 2 for the left/right borders
    self.score_x -= 2
    # Add home name x-position to align with name
    self.score_x += self.name_x

    self.score_y = self.name_y + 1

  def GetTeamNameStart(self):
    return (self.name_x, self.name_y)
  
  def GetTeamNameEnd(self):
    return (self.name_x + len(self.team_name) - 1, self.name_y)

  def GetScoreStart(self):
    return (self.score_x, self.name_y + 1)

  def GetScoreEnd(self):
    return (self.score_x + 3, self.name_y + 3)

  def GetScoreMid(self):
    return (self.score_x + 1, self.name_y + 2)

def main(stdscr):
  stdscr.clear()

  home_name = HOME_NAME
  home_logo = HOME_LOGO
  home_color = HOME_COLOR
  home_bgcolor = HOME_BGCOLOR

  curses.echo()
  stdscr.addstr(0, 0, 'Enter away team name: ')
  away_name = stdscr.getstr().decode('utf-8')

  curses.echo()
  stdscr.addstr(1, 0, 'Enter away team logo URL: ')
  away_logo = stdscr.getstr().decode('utf-8')

  curses.echo()
  stdscr.addstr(2, 0, 'Enter away team color (RGB, #HEX, "white"): ')
  away_color = stdscr.getstr().decode('utf-8')

  curses.echo()
  stdscr.addstr(3, 0, 'Enter away team background color (RGB, #HEX, "white"): ')
  away_bgcolor = stdscr.getstr().decode('utf-8')

  # Remove the directory if it already exists
  if os.path.isdir(SCORES_DIR):
    shutil.rmtree(SCORES_DIR)
  os.mkdir(SCORES_DIR)

  # Write out the CSS
  tmpl = Template(filename='common.css.mako', strict_undefined=True)
  contents = tmpl.render(
        home_color=home_color,
        home_bgcolor=home_bgcolor,
        away_color=away_color,
        away_bgcolor=away_bgcolor,

        # Calculate CSS manually since shotcut's renderer doesn't
        # handle them
        width=WIDTH,
        height=HEIGHT,

        border_width=HEIGHT // 12,

        timer_height=HEIGHT + 20,
        name_font=HEIGHT // 3,
        goals_height=HEIGHT - 20,
        goals_font=HEIGHT // 2.5,
  )
  with open(os.path.join(SCORES_DIR, 'common.css'), 'w') as f:
    f.write(contents)

  # Create template for the html
  tmpl = Template(filename='scoreboard.html.mako', strict_undefined=True)

  home_goals=0
  away_goals=0
  team=0

  stdscr.clear()
  curses.noecho()

  rectangle(stdscr, 5, 100, 25, 125)
  logs = 6

  written_files = set()

  keys = []

  while True:
    home = TeamScore(home_name, 2)
    stdscr.addstr(
      home.GetTeamNameStart()[1],
      home.GetTeamNameStart()[0],
      home_name)
    rectangle(
      stdscr,
      home.GetScoreStart()[1],
      home.GetScoreStart()[0],
      home.GetScoreEnd()[1],
      home.GetScoreEnd()[0])
    stdscr.addstr(
      home.GetScoreMid()[1],
      home.GetScoreMid()[0],
      str(home_goals))

    # Away team names should be at least 10 chars away from home team name
    away = TeamScore(away_name, home.GetTeamNameEnd()[0] + 10)
    stdscr.addstr(
      away.GetTeamNameStart()[1],
      away.GetTeamNameStart()[0],
      away_name)
    rectangle(
      stdscr,
      away.GetScoreStart()[1],
      away.GetScoreStart()[0],
      away.GetScoreEnd()[1],
      away.GetScoreEnd()[0])
    stdscr.addstr(
      away.GetScoreMid()[1],
      away.GetScoreMid()[0],
      str(away_goals))

    if team == 0:
      stdscr.move(home.GetScoreMid()[1], home.GetScoreMid()[0])
    else:
      stdscr.move(away.GetScoreMid()[1], away.GetScoreMid()[0])

    key = stdscr.getkey()
    keys.append(key)
    if key == 'KEY_RIGHT':
      team = 1
    elif key == 'KEY_LEFT':
      team = 0
    elif key == 'KEY_UP':
      if team == 0:
        home_goals += 1
      else:
        away_goals += 1
    elif key == 'KEY_DOWN':
      if team == 0:
        if home_goals > 0:
          home_goals -= 1
      else:
        if away_goals > 0:
          away_goals -= 1
    elif key == '\n':
      filename = '{}-{}.html'.format(home_goals, away_goals)
      if filename in written_files:
        continue
      written_files.update([filename])
      stdscr.addstr(logs, 101, 'Wrote {}'.format(filename))
      logs += 1

      contents = tmpl.render(
        home_logo=home_logo,
        home_name=home_name,
        home_goals=home_goals,
        away_logo=away_logo,
        away_name=away_name,
        away_goals=away_goals,
      )
      with open(os.path.join(SCORES_DIR, filename), 'w') as f:
        f.write(contents)
    elif key == 'q':
      break

if __name__ == '__main__':
  wrapper(main)
