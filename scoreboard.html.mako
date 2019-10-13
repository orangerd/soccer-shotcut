<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script src="qrc:/scripts/jquery.js"></script>
<script src="qrc:/scripts/rangy-core.js"></script>
<script src="qrc:/scripts/rangy-cssclassapplier.js"></script>
<script src="qrc:/scripts/htmleditor.js"></script>
<link rel="stylesheet" type="text/css" href="common_${timer}.css">
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
        <div class="goals">${away_goals}</div>
        <p class="name">${away_name}</p>
        <img src="${away_logo}" class="logo">
      </div>
    </div>
  </div>
</body>
</html>
