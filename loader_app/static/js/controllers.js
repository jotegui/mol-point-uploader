'use strict';

var loaderControllers = angular.module('loaderControllers', []);

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
        var path = $location.path();
        console.log(path);
        var api_key = '6132d3d852907530a3b047336430fc1999eb0f24';
        var q = "select title from point_uploads_registry where datasetid='829c1828-e128-480d-a863-bf28fd3396a2'";
        CartoDB.get({api_key: api_key, q: q},
            function success(response) {
                console.log("Success:"+JSON.stringify(response));
                $scope.title = response.rows[0].title;
            },
            function error(errorResponse){
                console.log("Error:"+JSON.stringify(errorResponse));
            }
        );
    }
]);