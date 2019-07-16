<html>
  <head>
  <meta http-equiv="content-type" content="text/html" charset="UTF-8">
  <title>MY SOUND</title>
  <link rel="shortcut icon" href="{{ url_for('static', filename='music.png') }}">
  <link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='css/style.css') }}">

  </head>
  <body>
    <div id="left-box">
      <div id="logo-image">
        <!-- <img src="static/icon_white.png" alt="icon" width="45"> -->
      My Sound
      <br><br><br><br>



      <div id='btn-search'>
        <a href="/" target="_blank">
            <img src="static/search.png" alt="icon" width="30" id="lib-icon" >
      検索
        </a>
      </div>

      <br>
      <div id='btn-search'>
        <img src="static/music_white.png" alt="icon" width="30" id="lib-icon" >
        My Library
      </div>

      <br>
      <div id='btn-search'>
        <a href="/sign_in" target="_blank">
        <img src="static/sign_in_white.png" alt="icon" width="30" id="lib-icon" >
        ユーザ登録
      </a>
      </div>


    </div>



    </div>
    <div id="right-box">
      <div class="search-boxes">

      </div>


    </div>

  </body>
</html>
