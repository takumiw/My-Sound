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
      <a href="/library" target="_blank">
        <img src="static/music_white.png" alt="icon" width="30" id="lib-icon" >
        My Library
      </a>

      <br><br>
      <!-- <a href="/sigh_in" target="_blank"> -->
      <div id='btn-search'>
        <img src="static/sign_in_white.png" alt="icon" width="30" id="lib-icon" >

        ユーザ登録
        </div>
      <!-- </a> -->


    </div>



    </div>


    <div id="right-box">
      <div class="search-boxes">
        メールアドレス  {{mail_address}} <br>
        ニックネーム  {{nick_name}} <br>
      </div>


    </div>

  </body>
</html>
