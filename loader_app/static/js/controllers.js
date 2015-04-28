'use strict';

var loaderControllers = angular.module('loaderControllers', ['infinite-scroll', 'ngTable']);

// Header form Controller (headers.html)
loaderControllers.controller('HeaderController', function(){

    // Store values in object
    this.headers = {};

    // Fields to check
    this.allheaders = ['scientificName', 'decimalLatitude', 'decimalLongitude', 'coordinateUncertaintyInMeters',/* 'geodeticDatum',*/ 'eventDate', 'recordedBy'];

    // Execute when clicking 'submit' button
    this.checkFields = function() {
        this.warning = "";
        console.log(this.headers);
        // Array to control duplicated fields
        this.fields = [];
        
        for (var i=0; i<this.allheaders.length; i++) {
            var key=this.allheaders[i];
            if (key=="scientificName") {
                var layman="scientific name";
            } else if (key=="decimalLatitude") {
                var layman="latitude";
            } else if (key=="decimalLongitude") {
                var layman="longitude";
            } else if (key=="coordinateUncertaintyInMeters") {
                var layman="uncertainty";
            } else if (key=="eventDate") {
                var layman="date and time";
            } else if (key=="recordedBy") {
                var layman="observer";
            }

            // Check missing fields with no default value
            // If a header is missing, 
            if (!(key in this.headers)) {
                // and a default value is absent
                if (!(key+"Default" in this.headers)) {
                    // Raise issue
                    if (this.warning == "") {
                        this.warning = "Warning: "+layman+" is missing, with no default value"
                   } 
                }
            }
            
            // Check if duplicated fields
            if (this.headers[key] != null && this.fields.indexOf(this.headers[key]) > -1) {
                if (this.warning=="") {
                    this.warning = "Warning: "+this.headers[key]+" appears more than once in the selected fields";
                }
            } else {
                this.fields.push(this.headers[key]);
            }
            
            // Specific check: eventDate corresponds with ISO8601 date
            if (key=="eventDate") {
                var regexIso8601 = /^(\d{4}|\+\d{6})(?:-(\d{2})(?:-(\d{2})(?:T(\d{2}):(\d{2}):(\d{2})\.(\d{1,})(Z|([\-+])(\d{2}):(\d{2}))?)?)?)?$/;
                var match;
                if (this.headers[key] == "") {
                    if (typeof this.headers[key+"Default"] === "string" && (match = this.headers[key+"Default"].match(regexIso8601))) {
                        console.log("date matches ISO");
                    } else {
                        if (this.warning=="") {
                            this.warning = "Warning: default value for eventDate is not a valid date";
                        }
                    }
                }
            }
        }
        
        // Only continue if there are no warnings
        if (this.warning == "") {
            document.forms["headerForm"].action = "store_headers";
            document.forms["headerForm"].submit();
        }
    }
});


// Metadata form controller, required to make the mandatory fields be mandatory
loaderControllers.controller('FormController', function() {});








// Record view page controller (records.html)
loaderControllers.controller('RecordController', ['$scope', '$location', '$filter', '$timeout', 'species', 'title', 'mapAvailable', 'points', 'ngTableParams',
    function RecordController($scope, $location, $filter, $timeout, species, title, mapAvailable, points, ngTableParams) {
        
        // extract and initialize variables
        $scope.tab = 'map';
        $scope.loading = true;
        $scope.speciesBtn = "All species";
        $scope.loadMoreText = "(scroll down to load more)";
        var path = $location.absUrl();
        $scope.dId = path.split("/")[path.split("/").length-1];
        $scope.selectedSpecies = "";
        $scope.species = $scope.allSpecies;
        $scope.search = {};

        // some functions
        $scope.updateFilter = function(value) {
            console.log($scope.speciesBtn);
            $scope.speciesBtn = value;
            if (value == 'All species') {
                value="";
                $scope.species = $scope.allSpecies;
            } else {
                $scope.species = value;
            };
            console.log($scope.species);
            $scope.search.scientificname = value;
            $scope.selectedSpecies = value;
            $scope.getPoints();
            $scope.map = $scope.resetMap($scope.map, value.replace(' ', '_'));            
        };

        // mapping functions
        var DEFAULT_CARTOCSS = "";
        DEFAULT_CARTOCSS += "#layer {";
        DEFAULT_CARTOCSS += "   marker-fill-opacity: 0.7;";
        DEFAULT_CARTOCSS += "   marker-line-color: #333333;";
        DEFAULT_CARTOCSS += "   marker-line-width: 1.5;";
        DEFAULT_CARTOCSS += "   marker-line-opacity: 0.8;";
        DEFAULT_CARTOCSS += "   marker-placement: point;";
        DEFAULT_CARTOCSS += "   marker-type: ellipse;";
        DEFAULT_CARTOCSS += "   marker-width: 10;";
        DEFAULT_CARTOCSS += "   marker-allow-overlap: true;";
        DEFAULT_CARTOCSS += "}";

        var DEFAULT_UNCERT_CARTOCSS = "";
        DEFAULT_UNCERT_CARTOCSS += "#layer {";
        DEFAULT_UNCERT_CARTOCSS += "  polygon-fill: #F84F40;";
        DEFAULT_UNCERT_CARTOCSS += "  polygon-opacity: 0.5;";
        DEFAULT_UNCERT_CARTOCSS += "  polygon-comp-op: darken;";
        DEFAULT_UNCERT_CARTOCSS += "  line-color: #FFF;";
        DEFAULT_UNCERT_CARTOCSS += "  line-width: 2;";
        DEFAULT_UNCERT_CARTOCSS += "  line-opacity: 0.8;";
        DEFAULT_UNCERT_CARTOCSS += "}";

        var stringToColour = function(str) {
            // str to hash
            for (var i = 0, hash = 0; i < str.length; hash = str.charCodeAt(i++) + ((hash << 5) - hash));
            // int/hash to hex
            for (var i = 0, colour = "#"; i < 3; colour += ("00" + ((hash >> i++ * 8) & 0xFF).toString(16)).slice(-2));
            return colour;
        }
        
        function getColor(d) {
            for (var i=0; i<$scope.species.length; i++) {
                if (d==$scope.species[i]) {
                    var color = stringToColour($scope.species[i])
                }
            }
            return color
        }
        
        $scope.createLegend = function(map) {
            var legend = L.control({position: 'topright'});
            $scope.labels = $scope.species;

            legend.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'info legend');//,
                    //grades = [],
                    //labels = species;
                // loop through our density intervals and generate a label with a colored square for each interval
                if (typeof $scope.species == "object") {
                    for (var i = 0; i < $scope.species.length; i++) {
                        div.innerHTML +=
                            '<i style="background:' + getColor($scope.species[i], $scope.species) + '"></i> ' + $scope.species[i] + '&nbsp <br>';
                    }
                } else {
                    div.innerHTML +=
                            '<i style="background:' + stringToColour($scope.species) + '"></i> ' + $scope.species + '&nbsp <br>';
                }

                return div;
            };

            legend.addTo(map);
        }

        $scope.createMapConfig = function() {
            var layers = [];
            var species_layer_id = 0;
            var species_layer_sql = "";
            var species_uncert_layer_sql = "";
            var colour_list = "";
            var selectedSpecies = "";
            if (typeof $scope.species == "object") {
                var species = $scope.species;
            } else {
                var species = [];
                species.push($scope.species);
            }


            console.log("mapConfig: "+species);
            if (species.length == 1) {
                selectedSpecies = species[0];
                species_layer_id = 1;
                species_layer_sql = "select * from point_uploads_master where datasetid='"+$scope.dId+"' and scientificname='"+selectedSpecies+"'";
                species_uncert_layer_sql = "SELECT cartodb_id, ST_Buffer(tt.the_geom_webmercator, tt.uncert) as the_geom_webmercator FROM ( SELECT COALESCE(coordinateuncertaintyinmeters, 5000) as uncert, * FROM point_uploads_master WHERE datasetid = '"+$scope.dId+"' and scientificname='"+selectedSpecies+"' ) tt";
                colour_list = "#layer{marker-fill: "+stringToColour(selectedSpecies)+";}";
                layers[0] = {
                    "type": "cartodb",
                    "options": {
                      "cartocss_version": "2.1.1",
                      "cartocss": "#layer{polygon-fill:#448833;polygon-opacity: 0.2;line-opacity:0.4;line-width:1;line-color: #448833;marker-fill-opacity: 0.2;marker-line-color: #448833;marker-line-width: 2;marker-line-opacity: 0.4;marker-placement: point;marker-type: ellipse;marker-width: 15;marker-fill: #448833;marker-allow-overlap: true;}",
                      "sql": "SELECT * FROM get_species_tile('"+selectedSpecies+"')"
                    }
                  }
            } else {
                species_layer_sql = "select row_number() over() as id, ST_Union(the_geom_webmercator) as the_geom_webmercator FROM point_uploads_master WHERE datasetid = '"+$scope.dId+"' GROUP BY  scientificname";
                species_uncert_layer_sql = "SELECT cartodb_id, ST_Buffer(tt.the_geom_webmercator, tt.uncert) as the_geom_webmercator FROM ( SELECT COALESCE(coordinateuncertaintyinmeters, 5000) as uncert, * FROM point_uploads_master WHERE datasetid = '"+$scope.dId+"' ) tt";
                colour_list = "#layer[id=1] {marker-fill: "+stringToColour(species[0])+";}";
                for (var i=1; i<species.length; i++) {
                    colour_list += "#layer[id="+(i+1)+"] {marker-fill: "+stringToColour(species[i])+";}";
                }
            }

            layers[species_layer_id] = {
                "type": "cartodb",
                "options": {
                  "cartocss_version": "2.1.1",
                  "cartocss": DEFAULT_UNCERT_CARTOCSS,
                  "sql": species_uncert_layer_sql
                }
              }
            layers[species_layer_id+1] = {
                "type": "cartodb",
                "options": {
                  "cartocss_version": "2.1.1",
                  "cartocss": DEFAULT_CARTOCSS + colour_list,
                  "sql": species_layer_sql
                }
              }

            var mapconfig = {
              "version": "1.0.1",
              "layers": layers
            }
            return mapconfig;
        }

        $scope.createMap = function() {
            
            // create map
            var map = new L.map('map_canvas').setView($scope.centroid, 3);
            
            // add base layer
            // 'https://dnv9my2eseobd.cloudfront.net/v3/cartodb.map-4xtxp73f/{z}/{x}/{y}.png'
            L.tileLayer('http://a.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: '&copy; <a href="http://www.mol.org">Map of Life</a>, 2014'
            }).addTo(map);
            
            // define mapconfig for ad-hoc anonymous map
            var mapconfig = $scope.createMapConfig();
            
            // initialize and attach ad-hoc map
            $.ajax({
              type: 'POST',
              dataType: 'json',
              contentType: 'application/json',
              url: 'https://mol.cartodb.com/api/v1/map',
              data: JSON.stringify(mapconfig),
              success: function(data) {
                var templateUrl = 'https://mol.cartodb.com/api/v1/map/' + data.layergroupid + '/{z}/{x}/{y}.png'
                L.tileLayer(templateUrl, {
                    maxZoom: 18
                }).addTo(map)
              }
            });

            $scope.createLegend(map, $scope.species);
            
            return map;
        }

        $scope.resetMap = function(map) {
            var selectedSpecies = "";
            map.remove();
            map = $scope.createMap($scope.species);
            return map;
        }




        // get all scientific names
        $scope.getSpecies = function() {
            species.get({q:$scope.dId},
                function success(response) {
                    console.log("Got species");
                    console.log(response.rows);
                    var allSpeciesJSON = response.rows;
                    $scope.allSpecies = [];
                    for (var i=0; i<allSpeciesJSON.length; i++) {
                        $scope.allSpecies.push(allSpeciesJSON[i].scientificname);
                    }
                },
                function error(errorResponse) {
                    console.log("Error getting species:"+JSON.stringify(errorResponse));
                }
            );
        }
        $scope.getSpecies();

        // get dataset title
        $scope.getTitle = function() {
            title.get({q:$scope.dId},
                function success(response) {
                    console.log("Got title");
                    $scope.title = response.rows[0].title;
                },
                function error(errorResponse){
                    console.log("Error getting dataset title:"+JSON.stringify(errorResponse));
                }
            );
        }
        $scope.getTitle();

        // get pres/abs of points
        $scope.getMapAvailable = function() {
            mapAvailable.get({q:$scope.dId},
                function success(response) {
                    var mapAvailable = response.rows[0].mapavailable;
                    $scope.mapAvailable = mapAvailable;
                    console.log("mapAvailable = "+mapAvailable);
                },
                function error(errorResponse){
                    console.log("Error checking if map should be rendered:"+JSON.stringify(errorResponse));
                }
            );
        }
        $scope.getMapAvailable();
        
        // get all points
        $scope.getPoints = function () {
            if ($scope.selectedSpecies != "") {
                var q2 = $scope.selectedSpecies;
            } else {
                var q2 = ""
            }
            points.get({q:$scope.dId, q2:q2},
                function success(response) {
                    
                    $scope.allPoints = response.rows;
                    console.log("Got "+$scope.allPoints.length+" records");
                    
                    // Map stuff
                    $scope.buildTable();

                    // Table stuff
                    if ($scope.loading === true) {
                        $scope.buildMap();
                    }

                    $scope.loading = false;
                },
                function error(errorResponse) {
                    console.log("Error getting points:"+JSON.stringify(errorResponse));
                }
            );
        }
        $scope.getPoints();


        $scope.buildTable = function() {
            // Infinite scroll (http://binarymuse.github.io/ngInfiniteScroll/)
            var offset = 0;
            var limit = 10;

            $scope.points = angular.copy($scope.allPoints.slice(0, limit));
            offset += limit;
            $scope.loadMore = function() {
                if (offset+limit>=$scope.allPoints.length) {
                    $scope.loadMoreText = "(all records loaded)";
                };
                if (offset<$scope.allPoints.length) {
                    if (offset+limit>$scope.allPoints.length) {
                        var chunk = $scope.allPoints.slice(offset);
                        console.log(chunk.length);
                    } else {
                        var chunk = $scope.allPoints.slice(offset, offset+limit);
                        offset += limit;
                    }
                    
                    for (var i = 0; i<chunk.length; i++) {
                        $scope.points.push(chunk[i]);
                    }
                }
            };
        }

        $scope.buildMap = function() {
            $scope.species = $scope.allSpecies;
            $scope.map = $scope.createMap();

            $timeout(function() {
                $scope.map.invalidateSize();
            });
        }
    }
]);
