'use strict';

// Service for querying CartoDB
var loaderServices = angular.module('loaderServices', ['ngResource']);

loaderServices.factory('CartoDB', ['$resource',
    function($resource){
        return $resource('https://mol.cartodb.com/api/v2/sql?api_key=6132d3d852907530a3b047336430fc1999eb0f24&q=:q', {}, {
            get:{method:'GET', isArray: false}
        });
    }
]);
