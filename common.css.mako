.body {
  margin: 0;
}

.container {
  border: 1px solid black;
  border-radius: 50px;
  left: 25px;
  position: absolute;
  top: 20px;
}

.base {
  --width: ${width}px;
  --height: ${height}px;
  --height: calc(var(--width) / 10);

  border: ${border_width}px solid white;
  border: calc(var(--height) / 12) solid white;
  border-radius: 50px;
  display: flex;
  font-family: Verdana;
  height: var(--height);
  overflow: hidden;
  width: var(--width);
}

.team {
  display: flex;
  flex: 1 0;
  text-align: center;
}

.home {
  background: ${home_bgcolor};
  color: ${home_color};
}

.away {
  background: ${away_bgcolor};
  color: ${away_color};
}

.timer {
  background-color: black;
  flex: 0 0 ${timer_height}px;
  flex: 0 0 calc(var(--height) + 20px);
}

.name {
  align-self: center;
  flex: 1;
  font-size: ${name_font}px;
  font-size: calc(var(--height) / 3);
}

.logo {
  flex: 0 0 var(--height);
  vertical-align: middle;
  width: var(--height);
}

.goals {
  align-self: center;
  background: white;
  border: 1px solid black;
  color: #000;
  flex: 0 0 ${goals_height}px;
  flex: 0 0 calc(var(--height) - 20px);
  font-size: ${goals_font}px;
  font-size: calc(var(--height) / 2.5);
  margin: 0 5px;
  padding: 5px 0;
}
