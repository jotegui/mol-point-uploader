(function() {
  
  // Main application
  var app = angular.module('loaderApp', []);
  
  // To avoid confusion between Jinja2 templates and AngularJS expressions
  // AngularJS expressions are now like {[{ expr }]}
  app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
  });
  
  // Header form Controller
  app.controller('HeaderController', function(){
    this.headers = {};
    this.checkFields = function() {
        this.warning = "";
        console.log(this.headers);
        this.fields = [];
        
        for (var key in this.headers) {
            if (this.fields.indexOf(this.headers[key]) > -1) {
                this.warning = "Warning: "+this.headers[key]+" appears more than once in the selected fields";
                
            } else {
                this.fields.push(this.headers[key]);
            }
        }
        if (this.warning == "" && this.fields.length<5) {
            this.warning = "Warning: Please make sure all required fields have a value";
        }
        if (this.warning == "") {
            document.forms["headerForm"].action = "metafields";
            document.forms["headerForm"].submit();
        }
    }
  });
  
  // Metadata form controller
  app.controller('FormController', function() {
  
  });
  
}) ();

