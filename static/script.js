  nblancer = 0;
  nbrevirement = 0;
  nbrebond = 0;
  nbfaute = 0;
  nbequipeL = 0;
  nbequipeA =0;
  {% for action in actions %}
    if (`{{action[1]}}`=="lancer"){
      nblancer +=1
    }
    else if (`{{action[1]}}`=="revirement"){
      nbrevirement +=1
    }
     else if (`{{action[1]}}`=="rebond"){
      nbrebond +=1
    }
     else if (`{{action[1]}}`=="faute"){
      nbfaute +=1
    }
    if (`{{action[2]}}`==`{{equipes[0]}}`){
      nbequipeL +=1
    }
    else if (`{{action[2]}}`== `{{equipes[1]}}`){
      nbequipeA +=1
    }
    
     {% endfor %}
      google.charts.load("current", {packages:["corechart"]});
      google.charts.setOnLoadCallback(drawChart);
      google.charts.setOnLoadCallback(drawChart2);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Action', 'Nombre'],
          ['Lancer', nblancer],
          ['Revirement',nbrevirement],
          ['Rebond', nbrebond],
          ['Faute', nbfaute],
        ]);

        var options = {
           title: "Répartition du nombre d'actions par type",
          pieHole: 0.4,
        };

        var chart = new google.visualization.PieChart(document.getElementById('donutchart'));
        chart.draw(data, options);
      }
      function drawChart2() {
        var data2 = google.visualization.arrayToDataTable([
          ['Equipe', "Nombre d'actions"],
          [`{{equipes[0]}}`, nbequipeL],
          [`{{equipes[1]}}`,nbequipeA],
        ]);

        var options = {
           title: "Répartition du nombre d'actions par équipe",
          pieHole: 0.4,
        };
        var chart2 = new google.visualization.PieChart(document.getElementById('donutchart2'));
        chart2.draw(data2, options);
      }
  