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

loaderServices.factory('species', ['$resource',
	function($resource) {
		return $resource('/api/species/:q', {}, {
			get:{method: 'GET', isArray:false}
		})
	}
]);

loaderServices.factory('title', ['$resource',
	function($resource) {
		return $resource('/api/title/:q', {}, {
			get:{method: 'GET', isArray:false}
		})
	}
]);

loaderServices.factory('mapAvailable', ['$resource',
	function($resource) {
		return $resource('/api/mapAvailable/:q', {}, {
			get:{method: 'GET', isArray:false}
		})
	}
]);

loaderServices.factory('points', ['$resource',
	function($resource) {
		return $resource('/api/points/:q/:q2', {}, {
			get:{method: 'GET', isArray:false}
		})
	}
]);