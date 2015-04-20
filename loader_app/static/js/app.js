'use strict';

// Main application
var loaderApp = angular.module('loaderApp', [
    'ngResource',
    'ngRoute',
    'loaderControllers',
    'loaderServices'
]);

// To avoid confusion between Jinja2 templates and AngularJS expressions
// AngularJS expressions are now like {[{ expr }]}
loaderApp.config(['$interpolateProvider', '$locationProvider',
    function($interpolateProvider, $locationProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
        $locationProvider.html5Mode(false).hashPrefix('!');
    }
]);
