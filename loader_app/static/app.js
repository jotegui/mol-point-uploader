(function() {
  
  // Main application
  var app = angular.module('loaderApp', []);
  
  // To avoid confusion between Jinja2 templates and AngularJS expressions
  // AngularJS expressions are now like {[{ expr }]}
  app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
  });
  
  // Header form Controller (headers.html)
  app.controller('HeaderController', function(){
    
    // Store values in object
    this.headers = {};
    
    // Fields to check
    this.allheaders = ['decimalLatitude', 'decimalLongitude', 'eventDate', 'recordedBy', 'scientificName'];
    
    // Execute when clicking 'submit' button
    this.checkFields = function() {
        this.warning = "";
        console.log(this.headers);
        // Array to control duplicated fields
        this.fields = [];
        
        for (var i=0; i<this.allheaders.length; i++) {
            var key=this.allheaders[i];

            // Check missing fields with no default value
            // If a header is missing, 
            if (!(key in this.headers)) {
                // and a default value is absent
                if (!(key+"Default" in this.headers)) {
                    // Raise issue
                    if (this.warning == "") {
                        this.warning = "Warning: "+key+" is missing, with no default value"
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
        }
        
        // Only continue if there are no warnings
        if (this.warning == "") {
            document.forms["headerForm"].action = "store_headers";
            document.forms["headerForm"].submit();
        }
    }
  });
  
  // Metadata form controller, required to make the mandatory fields be mandatory
  app.controller('FormController', function() {});
  
}) ();

