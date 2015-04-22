'use strict';

var loaderControllers = angular.module('loaderControllers', ['infinite-scroll']);

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
loaderControllers.controller('RecordController', ['$scope', '$location', 'CartoDB',
    function RecordController($scope, $location, CartoDB) {
        var path = $location.absUrl();
        var dId = path.split("/")[path.split("/").length-1];
        var q = "select title from point_uploads_registry where datasetid='"+dId+"'";
        CartoDB.get({q: q},
            function success(response) {
                console.log("Got title");
                $scope.title = response.rows[0].title;
            },
            function error(errorResponse){
                console.log("Error getting dataset title:"+JSON.stringify(errorResponse));
            }
        );

        q = "select count(*)>0 as mapAvailable from point_uploads_master where datasetid='"+dId+"'";
        CartoDB.get({q: q},
            function success(response) {
                var mapAvailable = response.rows[0].mapavailable;
                $scope.mapAvailable = mapAvailable;
                console.log("mapAvailable = "+mapAvailable);
            },
            function error(errorResponse){
                console.log("Error checking if map should be rendered:"+JSON.stringify(errorResponse));
            }
        );
        
        q = "select distinct scientificname from point_uploads_master where datasetid='"+dId+"'";
        CartoDB.get({q:q},
            function success(response) {
                console.log("Got species");
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
        
        q = "select scientificname, decimallatitude, decimallongitude, eventdate, recordedby, coordinateuncertaintyinmeters, geodeticdatum from point_uploads_master where datasetid='"+dId+"'";
        CartoDB.get({q:q},
            function success(response) {
                var allPoints = response.rows;
                var offset = 0;
                var limit = 10;
                
                console.log("Got "+allPoints.length+" records");
                
                
                // Map stuff
                
                
                
                // Table stuff
                
                $scope.points = angular.copy(allPoints.slice(0, limit));
                offset += limit;
                
                $scope.loadMore = function() {
                    if (offset<allPoints.length) {
                        if (offset+limit>allPoints.length) {
                            var chunk = allPoints.slice(offset);
                            console.log(chunk.length);
                        } else {
                            var chunk = allPoints.slice(offset, offset+limit);
                            offset += limit;
                        }
                        
                        for (var i = 0; i<chunk.length; i++) {
                            $scope.points.push(chunk[i]);
                        }
                    }
                };
            },
            function error(errorResponse) {
                console.log("Error getting points:"+JSON.stringify(errorResponse));
            }
        );
    }
]);
