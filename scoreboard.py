#!/usr/bin/env python3

from absl import app
from absl import flags

import curses
import os
import shutil

from curses import wrapper
from curses.textpad import rectangle

from mako.template import Template

from typing import Optional

FLAGS = flags.FLAGS

flags.DEFINE_string(
    'scores_dir',
    '/tmp/scores',
    'Directory to output scores. Note that it will be wiped out.')

flags.DEFINE_string(
    'home_name',
    'MVLA',
    'Name for the home team.')

flags.DEFINE_string(
    'home_logo',
    'https://spot70-images.s3.amazonaws.com/clubs/logos/000/000/022/thumb/mvla-logo.png',
    'Logo for the home team.')

flags.DEFINE_string(
    'home_color',
    '#ffffff',
    'Color for the home team.')

flags.DEFINE_string(
    'home_bgcolor',
    '#123764',
    'Background color for the home team.')

flags.DEFINE_string(
    'away_name',
    None,
    'Name for the away team.')

flags.DEFINE_string(
    'away_logo',
    None,
    'Logo for the away team.')

flags.DEFINE_string(
    'away_color',
    None,
    'Color for the away team.')

flags.DEFINE_string(
    'away_bgcolor',
    None,
    'Background color for the away team.')

flags.DEFINE_integer(
    'width',
    300,
    'Width of the scoreboard to show.')


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


def Prompt(stdscr, row: int, prompt: str) -> str:
  curses.echo()
  stdscr.addstr(row, 0, prompt)
  return stdscr.getstr().decode('utf-8')


def CursesWrapped(stdscr):
  stdscr.clear()

  i = 0

  width = FLAGS.width
  height = FLAGS.width // 10

  if FLAGS.away_name is None:
    away_name = Prompt(stdscr, i, 'Enter away team name: ')
    i += 1
  else:
    away_name = FLAGS.away_name

  if FLAGS.away_logo is None:
    away_logo = Prompt(stdscr, i, 'Enter away team logo URL: ')
    i += 1
  else:
    away_logo = FLAGS.away_logo

  if FLAGS.away_color is None:
    away_color = Prompt(
        stdscr,
        i,
        'Enter away team color (RGB, #HEX, "white"): ')
    i += 1
  else:
    away_color = FLAGS.away_color

  if FLAGS.away_bgcolor is None:
    away_bgcolor = Prompt(
        stdscr,
        i,
        'Enter away team background color (RGB, #HEX, "white"): ')
    i += 1
  else:
    away_bgcolor = FLAGS.away_bgcolor

  # Remove the directory if it already exists
  if os.path.isdir(FLAGS.scores_dir):
    shutil.rmtree(FLAGS.scores_dir)
  os.mkdir(FLAGS.scores_dir)

  # Write out the CSS
  tmpl = Template(filename='common.css.mako', strict_undefined=True)
  contents = tmpl.render(
        home_color=FLAGS.home_color,
        home_bgcolor=FLAGS.home_bgcolor,
        away_color=away_color,
        away_bgcolor=away_bgcolor,

        # Calculate CSS manually since shotcut's renderer doesn't
        # handle them
        width=width,
        height=height,

        border_width=height // 12,

        timer_height=height + 20,
        name_font=height // 3,
        goals_height=height - 20,
        goals_font=height // 2.5,
  )
  with open(os.path.join(FLAGS.scores_dir, 'common.css'), 'w') as f:
    f.write(contents)

  # Create template for the html
  tmpl = Template(filename='scoreboard.html.mako', strict_undefined=True)

  home_goals=0
  away_goals=0
  team=0

  stdscr.clear()
  curses.noecho()

  rectangle(stdscr, 5, 80, 25, 105)
  logs = 6

  written_files = set()

  keys = []

  while True:
    home = TeamScore(FLAGS.home_name, 2)
    stdscr.addstr(
      home.GetTeamNameStart()[1],
      home.GetTeamNameStart()[0],
      FLAGS.home_name)
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
      stdscr.addstr(logs, 82, 'Wrote {}'.format(filename))
      logs += 1

      contents = tmpl.render(
        home_logo=FLAGS.home_logo,
        home_name=FLAGS.home_name,
        home_goals=home_goals,
        away_logo=away_logo,
        away_name=away_name,
        away_goals=away_goals,
      )
      with open(os.path.join(FLAGS.scores_dir, filename), 'w') as f:
        f.write(contents)
    elif key == 'q':
      break


class FileWriter(object):
  def __init__(self, tmpl):
    self.tmpl = tmpl
    self.written_files = set()

  def WriteFile(self, home_goals: int, away_goals: int) -> Optional[str]:
    filename = '{}-{}.html'.format(home_goals, away_goals)
    if filename in self.written_files:
      return None
    self.written_files.update([filename])
    contents = self.tmpl.render(
      home_logo=FLAGS.home_logo,
      home_name=FLAGS.home_name,
      home_goals=home_goals,
      away_logo=away_logo,
      away_name=away_name,
      away_goals=away_goals,
    )
    with open(os.path.join(FLAGS.scores_dir, filename), 'w') as f:
      f.write(contents)
    return filename


def main(argv):
  wrapper(CursesWrapped)


if __name__ == '__main__':
  app.run(main)
