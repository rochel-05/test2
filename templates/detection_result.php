<!DOCTYPE html>
<html lang="en">
<head>
    <title>Resultats de la Detection</title>
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
                    <h3>Resultats De La Detection</h3>
                     {{ pagination.links }}
                    <table id="example" class="table table-hover table-bordered table-striped table-condensed" cellspacing="0" width="100%">
                    <tr>
                        <th>Frame</th>
                        <th>Resultat</th>
                        <th>Zone</th>
                        <th>Date&Hour</th>
                        <th>LPR</th>
                        <th>Alert Services</th>
                    </tr>
                    {% for result in results %}
                    <tr>
                        <td style="width:105px;height:105px;"><img src="/static/generated_frames_valid/{{result.frame}}" alt="crash image" width="105px" height="105px"></td>
                        <td class="error">{{ result.resultat }}</td>
                        <td class="sucess">{{ result.zone }}</td>
                        <td class="info">{{ result.date }}-{{ result.heure }}</td>
                        <!--<td>{{ loop.index + (page - 1) * per_page }}</td>-->
                        {% if result.resultat == 'Crash' %}
                        <td style="width:105px;height:105px;"><a href="/lpr/?frame={{result.frame}}" title="Reconnaitre une plaque" target="_blank"><img src="/static/img/lpr.jpg" alt="LPR" width="105px" height="105px"></a></td>
                        <td style="width:105px;height:105px;"><a href="/alert/" title="appeler les services d'urgence" target="_blank"><img src="/static/img/call.png" alt="crash image" width="105px" height="105px"></a></td>
                        {% endif %}
                    </tr>
                    {% endfor %}
                    </table>
                    {{ pagination.links }}
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