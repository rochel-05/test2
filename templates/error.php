<!DOCTYPE html>
<html lang="en">
<head>
    <title>Accueil</title>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" media="screen" href="/static/css/reset.css">
    <link rel="stylesheet" type="text/css" media="screen" href="/static/css/style.css">
    <link rel="stylesheet" type="text/css" media="screen" href="/static/css/grid_12.css">
    <link rel="stylesheet" type="text/css" media="screen" href="/static/css/slider.css">
    <link rel="stylesheet" href="/static/css/bootstrap.min.css" type="text/css"/>
    <link href='http://fonts.googleapis.com/css?family=Condiment' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Oxygen' rel='stylesheet' type='text/css'>
    <script type="text/javascript" src="{{ url_for('static', filename='jquery-1.7.min.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static', filename='jquery.easing.1.3.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static', filename='tms-0.4.x.js') }}"></script>
    <script>
		$(document).ready(function(){				   	
			$('.slider')._TMS({
				show:0,
				pauseOnHover:true,
				prevBu:false,
				nextBu:false,
				playBu:false,
				duration:1000,
				preset:'fade',
				pagination:true,
				pagNums:false,
				slideshow:7000,
				numStatus:true,
				banners:'fromRight',
				waitBannerAnimation:false,
				progressBar:false
			})		
		});
	</script>
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
                    <li><a href="contacts.php">Contacts</a></li>
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
        <div id="slide" class="box-shadow">		
            <div class="slider">
                <ul class="items">
                    <li><img src="/static/img/accident.jpg" alt="" /><div class="banner">Detection Des Accidents</div></li>
                    <li><img src="/static/img/Alerta.jpg" alt="" /><div class="banner">Alerte En Cas Des Urgences</div></li>
                    <li><img src="/static/img/lpr2.png" alt="" /><div class="banner">Detection Des Plaques D Immatriculation</div></li>
                </ul>
            </div>	
        </div>
        <div class="container_12">
          <div class="grid_12">
            <div class="pad-0 border-1" style="background-color:red;border-radius:4px;border:1px solid black;">
                <h2 class="top-1 p0">Desolé, Cette Page Ne Figure Dans Dans Cet Site!</h2>
                <p class="p2">
                    {% if code %}
                        <span style="text-decoration:blink;">Erreur : {{ code }}</span>
                    {% else %}
                        <span>Erreur Capturé Par Le Systeme</span>
                    {% endif %}
                </p>
            </div>
            <div class="wrap block-1 pad-1">
                <div>
                    <h3>Detection Accident</h3>
                    <img src="/static/img/collision.jpg" alt="" class="img-border">
                    <p>Nous vous rendons facile votre vie en offrant un technique de detection d accident pour sauver les gens et pour stabiliser la circuit routiere.</p>
                    <a href="#" class="button">More</a>
                </div>
                <div>
                    <h3>Alerte Urgent</h3>
                    <img src="/static/img/hopital2.jpg" alt="" class="img-border">
                    <p>Notre Service vous offre un moyen rapide pour alerter des services d urgence en cas d urgence.</p>
                    <a href="#" class="button">More</a>
                </div>
                <div class="last">
                    <h3>Detection De Plaque</h3>
                    <img src="/static/img/nlp2.PNG" alt="" class="img-border">
                    <p>Nous vous offre un moyen de securisation pendant votre voyage en identifiant votre immatriculation.</p>
                    <a href="#" class="button">More</a>
                </div>
            </div>
          </div>
          <div class="clear"></div>
        </div>
    </section> 
  </div>    
<!--==============================footer=================================-->
    <footer>
        <p>© 2019 Direction Generale De La Securité Routiere Madagascar (DGSR)</p>
        <p><a href="https://www.presidence.gov.mg/" target="_blank" rel="nofollow">Gouvernement Malagasy</a></p>
    </footer>	    
</body>
</html>