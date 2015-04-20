'use strict';

// Service for querying CartoDB
var loaderServices = angular.module('loaderServices', ['ngResource']);

loaderServices.factory('CartoDB', ['$resource',
    function($resource){
        return $resource('https://mol.cartodb.com/api/v2/sql?api_key=:api_key&q=:q', {}, {
            get:{method:'GET', isArray: false}
        });
    }
]);
