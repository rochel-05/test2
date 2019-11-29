<!DOCTYPE html>
<html lang="en">
<head>
    <title>Systeme D Alerte</title>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" media="screen" href="/static/css/reset.css">
    <link rel="stylesheet" type="text/css" media="screen" href="/static/css/style.css">
    <link rel="stylesheet" type="text/css" media="screen" href="/static/css/grid_12.css">
    <link rel="stylesheet" href="/static/css/bootstrap.min.css" type="text/css"/>
    <link rel="stylesheet" href="/static/css/bootstrap-responsive.min.css" type="text/css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css">
    <link href='http://fonts.googleapis.com/css?family=Condiment' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Oxygen' rel='stylesheet' type='text/css'>
    <script type="text/javascript" src="{{ url_for('static', filename='jquery-1.7.min.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static', filename='jquery.easing.1.3.js') }}"></script>
	<!--[if lt IE 8]>
       <div style=' clear: both; text-align:center; position: relative;'>
         <a href="http://windows.microsoft.com/en-US/internet-explorer/products/ie/home?ocid=ie6_countdown_bannercode">
           <img src="http://storage.ie6countdown.com/assets/100/images/banners/warning_bar_0000_us.jpg" border="0" height="42" width="820" alt="You are using an outdated browser. For a faster, safer browsing experience, upgrade for free today." />
        </a>
      </div>
    <![endif]-->
    <!--[if lt IE 9]>
   		<script type="text/javascript" src="{{ url_for('static', filename='html5.js') }}"></script>
    	<link rel="stylesheet" type="text/css" media="screen" href="/static/css/ie.css">
	<![endif]-->
</head>
<body>
  <div class="main">
  <!--==============================header=================================-->
    <header>
       <h1><a href="/"><img src="/static/img/dgsr.png" alt=""></a></h1>
        <div class="form-search">
            <form id="form-search" method="post">
                <input type="text" value="Tapez ici..." onBlur="if(this.value=='') this.value='Tapez ici...'" onFocus="if(this.value =='Tapez ici...' ) this.value=''"  />
              <a href="#" onClick="document.getElementById('form-search').submit()" class="search_button"></a>
            </form>
        </div>   
        <div class="clear"></div>    
        <nav class="box-shadow">
            <div>
                <ul class="menu">
                    <li class="home-page current"><a href="/">Accueil</a></li>
                    <li><a href="/detection/">Crash Detection</a></li>
                    <li><a href="/accuracy/">Accuracy Results</a></li>
                    <li><a href="/emergency/">Emergency Alert</a></li>
                    <!--<li><a href="contacts.php">Contacts</a></li>-->
                    <li><a href="/logout/">Log Out</a></li>
                </ul>
                <div class="social-icons">
                    <span>Follow us:</span>
                    <a href="#" class="icon-3"></a>
                    <a href="#" class="icon-2"></a>
                    <a href="#" class="icon-1"></a>
                </div>
                <div class="clear"></div>
            </div>
        </nav>
    </header>   
  <!--==============================content================================-->
    <section id="content">
        <div class="container_12">	
          <div class="grid_12">
            <div class="wrap pad-3">
                <div class="block-5" style="width:900px;">
                    <h3>Systeme D Alerte</h3>
                       <div class="map img-border" style="width:900px;">
                           {% if src %}
                                <iframe src='{{ src }}' width='853' height='480' frameborder=0, allowfullscreen class="img-polaroid" style="width:900px;"></iframe>
                           {% else %}
                                <iframe src='https://www.youtube.com/embed/OuNcwwaaqRc' width='853' height='480' frameborder=0, allowfullscreen class="img-polaroid" style="width:900px;"></iframe>
                           {% endif %}
                        </div>
                       <form id="form" method="post" action="/urgence/">
                      <fieldset>
                        <div class="btns">
                            <input type="submit" value="Alerter" class="button" onClick="document.getElementById('form').submit()" style="width:100px;height:30px; background-color:rgb(0,138,138);"/>
                        </div>
                      </fieldset>
                      </form>
                </div>
            </div>
          </div>
          <div class="clear"></div>
        </div>
    </section> 
  </div>    
<!--==============================footer=================================-->
  <footer>
      <p>© 2019 Direction Des Systemes D Information Madagascar (DSI)</p>
      <p><a href="https://www.presidence.gov.mg/" target="_blank" rel="nofollow">Gouvernement Malagasy</a></p>
  </footer>
</body>
</html>