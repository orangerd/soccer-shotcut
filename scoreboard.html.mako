<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script src="qrc:/scripts/jquery.js"></script>
<script src="qrc:/scripts/rangy-core.js"></script>
<script src="qrc:/scripts/rangy-cssclassapplier.js"></script>
<script src="qrc:/scripts/htmleditor.js"></script>
<style>
.body {
  margin: 0;
}

.container {
  border: 1px solid black;
  border-radius: 50px;
  left: -125px;
  position: absolute;
  top: 20px;
  transform: scale(0.5, 0.7);
  width: 580px;
}

.base {
  border: 5px solid white;
  border-radius: 50px;
  font-family: Verdana;
  overflow: hidden;
  height: 60px;
}

.team {
  float: left;
  height: 100%;
  line-height: 35px;
  text-align: center;
  width: 43%;
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
  float: left;
  height: 100%;
  width: 14%;
}

.home * {
  float: left;
}
.away * {
  float: right;
}

.name {
  margin: 10px 0px 0px 5px;
  font-size: 20px;
}

.logo {
  vertical-align: middle;
  width: 60px;
}

.goals {
  background: white;
  box-shadow: 0px 0px 0px 1px black;
  color: #000;
  font-size: 24px;
  height: 40px !important;
  margin: 10px 5px;
  width: 40px;
}
.home .goals {
  float: right;
}
.away .goals {
  float: left;
}
</style>
</head>
<body>
  <div class="container">
    <div class="base">
      <div class="team home">
        <img src="${home_logo}" class="logo">
        <p class="name">${home_name}</p>
        <div class="goals">${home_goals}</div>
      </div>
      <div class="timer">&nbsp;</div>
      <div class="team away">
        <img src="${away_logo}" class="logo">
        <p class="name">${away_name}</p>
        <div class="goals">${away_goals}</div>
      </div>
    </div>
  </div>
</body>
</html>
