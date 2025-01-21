import streamlit as st
import streamlit.components.v1 as components


#uploaded_file = st.file_uploader("./data/covid19-data.csv")
#print(f"uploaded_file: {uploaded_file}")

# JavaScript code from WorldCOVID19BubbleMapPlot-Test1.js
js_code = """
//get the date string for today
var strdate = getOffsetDate(0, "mm-dd-yyyy");
console.log(strdate);

var valuesGroupByColumn;
//nst groupByColumn = "Country/Region";
//nst aggType = "sum";

const strCityColName = 'Province_State';
const strCountryColName = 'Country_Region';
//const strLongColName = 'Long_';
//const strLatColName = 'Lat';
const strLongColName = 'Longitude';
const strLatColName = 'Latitude';

const groupByColumn = strCountryColName;
const aggType = "sum";


//download csv source data and then make scattergeo plot and generate jexcel table
Plotly.d3.csv(
    "https://raw.githubusercontent.com/anthonylai2046/my_component/main/data/covid19-data.csv",
    //"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" + strdate + ".csv",
    //"http://localhost:8501/data/covid19-data.csv",
    //"/data/covid19-data.csv",
    //"01-20-2025.csv",
    //"covid19-data.csv",
    //[UPLOADED_FILE],
    function(err, rows) {
        if(err == null)
        {
            console.log(strdate);
            strdate = getOffsetDate(0, "yyyy-mm-dd"); //change the date format to "yyyy-mm-dd" for displaying on the heading of the scattergeo chart
            console.log(rows.length);
            console.log(rows[0]);
            makePlot(err, rows, strdate);
            groupByData(rows, groupByColumn, aggType)
            makeTable(rows);
        }
        else
        {
            //get the date string for yesterday
            strdate = getOffsetDate(1, "mm-dd-yyyy");
            console.log(strdate);
            Plotly.d3.csv(
                "https://raw.githubusercontent.com/anthonylai2046/my_component/main/data/covid19-data.csv",
                //"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" + strdate + ".csv",
                //"http://localhost:8501/data/covid19-data.csv",
                //"/data/covid19-data.csv",
                //"01-20-2025.csv",
                //"covid19-data.csv",
                //[UPLOADED_FILE],
                function(err, rows) {
                    strdate = getOffsetDate(1, "yyyy-mm-dd"); //change the date format to "yyyy-mm-dd" for displaying on the heading of the scattergeo chart
                    console.log(rows.length);
                    console.log(rows[0]);
                    makePlot(err, rows, strdate);
                    groupByData(rows, groupByColumn, aggtype)
                    makeTable(rows);
                }
            );
        }
    }
);


//function for create the plotly scattergeo plot
function makePlot(err, rows, strdate)
{
        console.log("Before create COVID-19 World Map");
        //console.log(err);
        //console.log(rows);

        function unpack(rows, key) {
            console.log(key);
            return rows.map(function(row) {
                return row[key];
            });
        };
        
        
        function getSum(total, num) {
          return total + Math.round(num);
        }


        
/* 		var cityName = unpack(rows, 'Province/State'),
            countryName = unpack(rows, 'Country/Region'),
            cityCases = unpack(rows, 'Confirmed'),
            cityDeaths = unpack(rows, 'Deaths'),
            cityRecovered = unpack(rows, 'Recovered'),
            cityLat = unpack(rows, 'Latitude'),
            cityLon = unpack(rows, 'Longitude'),
            hoverText = []; */
            
        var cityName = unpack(rows, strCityColName),
            countryName = unpack(rows, strCountryColName),
            cityCases = unpack(rows, 'Confirmed'),
            cityDeaths = unpack(rows, 'Deaths'),
            cityRecovered = unpack(rows, 'Recovered'),
            cityLat = unpack(rows, strLatColName),
            cityLon = unpack(rows, strLongColName),
            hoverText = [];
        
        //calculate the Total Confirmed Cases and Total Deaths Cases
        const arrcityCasesSum = cityCases.reduce(getSum, 0);
        const arrcityDeathsSum = cityDeaths.reduce(getSum, 0);

        //console.log(arrcityCasesSum);
        
        //prepare for hover text for each city in a country or just country
        for ( var i = 0 ; i < cityCases.length; i++) {
            var currentText = "";
            var cityActive = cityCases[i] - cityDeaths[i] - cityRecovered[i]
            if(cityName[i] == "")
                currentText = countryName[i] + "<br>Confirmed: " + cityCases[i] + "<br>Deaths: " + cityDeaths[i] + "<br>Recovered: " + cityRecovered[i] + "<br>Active: " + cityActive;
            else
                currentText = cityName[i] + ", " + countryName[i] + "<br>Confirmed: " + cityCases[i] + "<br>Deaths: " + cityDeaths[i] + "<br>Recovered: " + cityRecovered[i] + "<br>Active: " + cityActive;
            hoverText.push(currentText);
        }

        //trace1: Confirmed Cases > 100,000
        var trace0 = 
            {
                //name: 'Confirmed > 100,000',
                name: 'Confirmed > 1,000,000',
                type: "scattergeo",
                mode: 'markers',
                hoverinfo: 'text',
                text: hoverText,
                lon: cityLon,
                lat: cityLat,
                
                //marker: { color: "fuchsia", size: 4 },
                marker: {
                    //color: "fuchsia",
                    color: "rgb(40, 0, 0)",
/* 					colorscale: scl1,
                    cmin: 10000,
                    color: unpack(rows, 'Cases'),
                    colorbar: {
                        title: 'COVID-19 Confirmed Cases'
                    }, */
                    opacity: 0.8,
                    autocolorscale: false,
                    size: cityCases,
                    sizemode: "area",
                    sizeref: 40 // size ref for value > 100,000
                },
                transforms: [
                  {	type: 'filter',
                    target: cityCases,
                    operation: '>',
                    value: 1000000
                  }
                ]
            };
            

        //trace0_1: 50,000 < Confirmed Cases <= 100,000
        var trace0_1 = 
            {
                //name: '50,000 < Confirmed <= 100,000',
                name: '500,000 < Confirmed <= 1,000,000',
                type: "scattergeo",
                mode: 'markers',
                hoverinfo: 'text',
                text: hoverText,
                lon: cityLon,
                lat: cityLat,
                
                //marker: { color: "fuchsia", size: 4 },
                marker: {
                    //color: "fuchsia",
                    color: "rgb(70, 0, 0)",
/* 					colorscale: scl1,
                    cmin: 10000,
                    color: unpack(rows, 'Cases'),
                    colorbar: {
                        title: 'COVID-19 Confirmed Cases'
                    }, */
                    opacity: 0.8,
                    autocolorscale: false,
                    size: cityCases,
                    sizemode: "area",
                    sizeref: 35 // size ref for 50,000 < value <= 100,000
                },
                transforms: [
                  {	type: 'filter',
                    target: cityCases,
                    operation: '<=',
                    value: 10000000
                  },
                  {	type: 'filter',
                    target: cityCases,
                    operation: '>',
                    value: 500000
                  }
                ]
            };			

        //trace1: 10,000 < Confirmed Cases <= 50,000
        var trace1 = 
            {
                //name: '10,000 < Confirmed <= 50,000',
                name: '100,000 < Confirmed <= 500,000',
                type: "scattergeo",
                mode: 'markers',
                hoverinfo: 'text',
                text: hoverText,
                lon: cityLon,
                lat: cityLat,
                
                //marker: { color: "fuchsia", size: 4 },
                marker: {
                    //color: "fuchsia",
                    color: "rgb(120, 0, 0)",
/* 					colorscale: scl1,
                    cmin: 10000,
                    color: unpack(rows, 'Cases'),
                    colorbar: {
                        title: 'COVID-19 Confirmed Cases'
                    }, */
                    opacity: 0.8,
                    autocolorscale: false,
                    size: cityCases,
                    sizemode: "area",
                    sizeref: 30 // size ref for 10,000 < value <= 50,000
                },
                transforms: [
                  {	type: 'filter',
                    target: cityCases,
                    operation: '<=',
                    value: 500000
                  },
                  {	type: 'filter',
                    target: cityCases,
                    operation: '>',
                    value: 100000
                  }
                ]
            };

        //trace2: 1,000 < Confirmed Cases <= 10,000
        var trace2 = 
            {
                //name: '1,000 < Confirmed <= 10,000',
                name: '10,000 < Confirmed <= 100,000',
                type: "scattergeo",
                mode: 'markers',
                hoverinfo: 'text',
                text: hoverText,
                lon: cityLon,
                lat: cityLat,
                //marker: { color: "fuchsia", size: 4 },
                marker: {
                    //color: "fuchsia",
                    color: "rgb(170, 0, 0)",
/* 					colorscale: scl2,
                    cmin: 1000,
                    color: unpack(rows, 'Cases'),
                    colorbar: {
                        title: 'COVID-19 Confirmed Cases'
                    },
 */					opacity: 0.8,
                    autocolorscale: false,
                    size: unpack(rows, 'Confirmed'),
                    sizemode: "area",
                    sizeref: 18 // size ref for 1,000 < value <= 10,000
                },
                transforms: [
                  {	type: 'filter',
                    target: cityCases,					operation: '<=',
                    value: 100000
                  },
                  {	type: 'filter',
                    target: cityCases,
                    operation: '>',
                    value: 10000
                  }

                ]
            };

        //trace3: 100 < Confirmed Cases <= 1,000
        var trace3 = 
            {
                //name: '100 < Confirmed <= 1,000',
                name: '1000 < Confirmed <= 10,000',
                type: "scattergeo",
                mode: 'markers',
                hoverinfo: 'text',
                text: hoverText,
                lon: cityLon,
                lat: cityLat,
                //marker: { color: "fuchsia", size: 4 },
                marker: {
                    //color: "fuchsia",
                    color: "rgb(255, 0, 0)",
/* 					colorscale: scl2,
                    cmin: 1000,
                    color: unpack(rows, 'Cases'),
                    colorbar: {
                        title: 'COVID-19 Confirmed Cases'
                    },
 */					opacity: 0.8,
                    autocolorscale: false,
                    size: unpack(rows, 'Confirmed'),
                    sizemode: "area",
                    sizeref: 3 // size ref for 100 < value <= 1,000
                },
                transforms: [
                  {	type: 'filter',
                    target: cityCases,
                    operation: '<=',
                    value: 10000
                  },
                  {	type: 'filter',
                    target: cityCases,
                    operation: '>',
                    value: 1000
                  }
                ]
            };

        //trace4: 1 <= Confirmed Cases <= 100
        var trace4 = 
            {
                //name: '1 < Confirmed <= 100',
                name: '100 < Confirmed <= 1,000',
                type: "scattergeo",
                mode: 'markers',
                hoverinfo: 'text',
                text: hoverText,
                lon: cityLon,
                lat: cityLat,
                //marker: { color: "fuchsia", size: 4 },
                marker: {
                    //color: "fuchsia",
                    //color: "rgb(255, 192, 204)",
                    color: "rgb(204, 51, 192)",
/* 					colorscale: scl2,
                    cmin: 1000,
                    color: unpack(rows, 'Cases'),
                    colorbar: {
                        title: 'COVID-19 Confirmed Cases'
                    },
 */					opacity: 0.8,
                    autocolorscale: false,
                    size: unpack(rows, 'Confirmed'),
                    sizemode: "area",
                    sizeref: 1.0// size ref for 0 <= value <= 100
                },
                transforms: [
                  {	type: 'filter',
                    target: cityCases,
                    operation: '<=',
                    value: 1000
                  },
                  {	type: 'filter',
                    target: cityCases,
                    operation: '>',
                    value: 100
                  }
                ]
            };


        var layout = 
        {
          geo: {
            showland: true, 
            showlakes: true, 
            showocean: true, 
            //projection: {type: 'orthographic'},
            //projection: {type: 'natural earth'},
            //projection: {type: 'equirectangular'},
            //projection: {type: 'kavrayskiy7'},
            //projection: {type: 'robinson'},
            //projection: {type: 'miller'},
            //projection: {type: 'azimuthal equal area'},
            //projection: {type: 'albers usa'},
            //projection: {type: 'mercator'},
            //scope: 'asia',
            //scope: 'usa',
            //scope: 'europe',
            //scope: 'africa',
            //scope: 'north america',
            //scope: 'south america',
            //scope: 'world',
            showrivers: true, 
            showcountries: true,
            landcolor: 'lightgray',
            oceancolor: '#e8f4f8',
          },
          legend: {
            x: 0.5,
            xref: 'paper',
            xanchor: 'center',
            //y: 1,
            //yanchor: 'top',
            orientation: "h"
          },
          title: {
            text: '<b>COVID-19 Global Confirmed Cases on ' + strdate + ' (by Anthony Lai)</b><br>' + '<b>Total Confirmed: ' + arrcityCasesSum.toLocaleString('en-US') + '</b>' + '      <b>Total Deaths: ' + arrcityDeathsSum.toLocaleString('en-US') + '</b>',
            font: {
              family: 'Courier New, monospace',
              size: 22,
              color: 'red'
            },
            xref: 'paper',
            x: 1.05,
          },
          hovermode: 'closest',
          height: 610,
          
          
          updatemenus: [
            {
                //An update button to update the geo: scope
                buttons: [
                {
                    args: [{geo: { scope: ''}}],
                    label: 'Update',
                    method: 'update'
                },
                ],
                showactive: true,
                type: 'buttons',
                x: 0.0002,
                y: 1.10,
                xref: 'paper',
                yref: 'paper',
                yanchor: 'auto',
                font: {color: '#5072a8'}
            },
            //A set of dropdown button to change geo: scope
            {
                x: 0.0002,
                y: 1.010,
                xref: 'paper',
                yref: 'paper',
                yanchor: 'auto',
                active: 0,
                showactive: true,
                buttons: [
                {
                    args: [{geo: { showland: true, showlakes: true, showocean: true, scope: 'world', showrivers: true, showcountries: true, landcolor: 'lightgray', oceancolor: '#e8f4f8'}}],
                    label: 'World',
                    method: 'relayout',
                }, {
                    args: [{geo: { showland: true, showlakes: true, showocean: true, scope: 'usa', showrivers: true, showcountries: true, landcolor: 'lightgray', oceancolor: '#e8f4f8'}}],
                    label: 'USA',
                    method: 'relayout',
                }, {
                    args: [{geo: { showland: true, showlakes: true, showocean: true, scope: 'europe', showrivers: true, showcountries: true, landcolor: 'lightgray', oceancolor: '#e8f4f8'}}],
                    label: 'Europe',
                    method: 'relayout',
                }, {
                    args: [{geo: { showland: true, showlakes: true, showocean: true, scope: 'asia', showrivers: true, showcountries: true, landcolor: 'lightgray', oceancolor: '#e8f4f8'}}],
                    label: 'Asia',
                    method: 'relayout',
                }, {
                    args: [{geo: { showland: true, showlakes: true, showocean: true, scope: 'africa', showrivers: true, showcountries: true, landcolor: 'lightgray', oceancolor: '#e8f4f8'}}],
                    label: 'Africa',
                    method: 'relayout',
                }, {
                    args: [{geo: { showland: true, showlakes: true, showocean: true, scope: 'north america', showrivers: true, showcountries: true, landcolor: 'lightgray', oceancolor: '#e8f4f8'}}],
                    label: 'North America',
                }, {
                    args: [{geo: { showland: true, showlakes: true, showocean: true, scope: 'south america', showrivers: true, showcountries: true, landcolor: 'lightgray', oceancolor: '#e8f4f8'}}],
                    label: 'South America',
                    method: 'relayout',
                }]
            }]
        };
        
        
        var config = {responsive: true, displayModeBar: false}; //hide the plotly menubar
        
        //var data = [trace0, trace0_1, trace1, trace2, trace3, trace4];
        var data = [trace0_1, trace1, trace2, trace3, trace4];
        //var data = [trace1, trace2, trace3, trace4];
        
        Plotly.newPlot("myDiv", data, layout, config);
        
};


//function to sum(Confirmed), sum(Deaths), sum(Recovered) with group by Country and sorted by sum(Confirmed)
function groupByData(data, groupByColumn, aggType)
{
    data.forEach(function(d){
        //group and organize the data as needed here
      valuesGroupByColumn = d3.nest()
      //set the groupByColumn as the key
      .key(function(d) {return d[groupByColumn];}) 
      //rollup and sum the cases values by groupByColumn
      .rollup((function(d) {
        return {
            Confirmed: d3.sum(d, function(e) { return e["Confirmed"]; }),
            Deaths: d3.sum(d, function(e) { return e["Deaths"]; }),
            Recovered: d3.sum(d, function(e) { return e["Recovered"]; }),
        };
      }))
      .entries(data);
    });
    
    //Re-arrange GroupBy Data
    var newData = [];
    var rows = valuesGroupByColumn;
    for (var key in rows) { 
        if (rows.hasOwnProperty(key) && rows[key].value['Confirmed'] >= 1) {
            var tmp = {}
            //var tmp = rows[key].value;
            tmp["Country"] = rows[key].key;
            tmp["Confirmed"] = rows[key].value['Confirmed'];
            tmp["Deaths"] = rows[key].value['Deaths'];
            tmp["Recovered"] = rows[key].value['Recovered'];
            tmp["Active"] = tmp["Confirmed"] - tmp["Deaths"] - tmp["Recovered"];
            //console.log(tmp)
            newData.push(tmp);
        } 
    }
    
    //Sort the data by descending
    newData = newData.sort(function(a, b) {
        return d3['descending'](a.Confirmed, b.Confirmed);
        //return d3['descending'](a.Deaths, b.Deaths);
        //return d3['descending'](a.Recovered, b.Recovered);
    });
    
    //assign the new data to valuesGroupByColumn
    valuesGroupByColumn = newData;
}

//function to create the jexcel table sorted by Confirmed Cases descending
function makeTable(rows)
{
    console.log("Before create jexcel table");
    //console.log(valuesGroupByColumn);
    jexcel(document.getElementById('myTable'), {
        data: valuesGroupByColumn,
        csvHeaders: true,
        search: true,
        pagination: 15,
        columns: [
            { type:'text', width:250, title:'Country'},
            { type:'text', width:150, title:'Confirmed'},
            { type:'text', width:150, title:'Deaths'},
            { type:'text', width:150, title:'Recovered'},
            { type:'text', width:150, title:'Active'},
         ]
    });
}


//function to get date string with offset and format
function getOffsetDate(offset, format) {
    var tday;
    var today = new Date();

    today.setDate(today.getDate() - offset);
    var dd = today.getDate();

    var mm = today.getMonth()+1; 
    var yyyy = today.getFullYear();

    if(dd<10) 
    {
        dd='0'+dd;
    } 

    if(mm<10) 
    {
        mm='0'+mm;
    }
    
    if(format == "yyyy-mm-dd")
        tday = yyyy + '-' + mm + '-' + dd;
    else if (format == "mm-dd-yyyy")
        tday = mm + '-' + dd + '-' + yyyy;
    else
        tday = yyyy + '-' + mm + '-' + dd;

    return tday;
}
"""

#print(f"uploaded_file: {uploaded_file}")
#if uploaded_file is not None:
#    js_code = js_code.replace("[UPLOADED_FILE]", uploaded_file.name)


# Bootstrap + Custom HTML Integration
bootstrap_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
    <!-- Load plotly.js into the DOM -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

    <!-- Load d3.js into the DOM -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/5.15.0/d3.min.js"></script>

    <script src="https://bossanova.uk/jexcel/v4/jexcel.js"></script>
    <link rel="stylesheet" href="https://bossanova.uk/jexcel/v4/jexcel.css">
    <!-- Load jexcel.js, jexcel.css, jsuites.css and jexcel.datatables.css into the DOM -->
    <script src="https://bossanova.uk/jexcel/v3/jexcel.js"></script>
    <script src="https://bossanova.uk/jsuites/v2/jsuites.js"></script>
    <link rel="stylesheet" href="https://bossanova.uk/jexcel/v3/jexcel.css" type="text/css" />
    <link rel="stylesheet" href="https://bossanova.uk/jsuites/v2/jsuites.css" type="text/css" />
    <link rel="stylesheet" href="https://bossanova.uk/jexcel/v3/jexcel.datatables.css" type="text/css" />
    <script>
        {js_code}
    </script>
</head>
<body>
    <div id="myDiv"></div>
    <div id="myTable"></div>
    
</body>
</html>
"""

# Render the Bootstrap + Plotly + jExcel content in Streamlit
components.html(bootstrap_html, height=1500, width = 1000)