mainApplication = angular.module('mainApplication', ['ngRoute','chart.js', 'ngMessages']);

mainApplication.config(function($routeProvider) {
    $routeProvider.when('/', {
                    templateUrl : 'pages/welcome.html'
                }).when('/Welcome', {
                    templateUrl : 'pages/welcome.html'
                }).when('/Data', {
                    templateUrl : 'pages/data.html'
                    ,controller  : 'dataController'
                }).when('/Shutter', {
                    templateUrl : 'pages/shutter.html'
                    ,controller  : 'shuttleController'
                }).when('/Airing', {
                    templateUrl : 'pages/airing.html'
                    ,controller  : 'airingController'
                }).when('/Configuration', {
                    templateUrl : 'pages/configuration.html'
                    ,controller  : 'configurationController'
                }).when('/Log', {
                    templateUrl : 'pages/log.html'
                    ,controller  : 'logController'
                })
});

mainApplication.config(['$httpProvider',function($httpProvider) {
    $httpProvider.defaults.timeout = 50000;
    $httpProvider.interceptors.push(function ($q, $location, $injector, serverMonitoring) {
        return {
            'request': function(request) {            	
            	console.log('request')
                serverMonitoring.startToWait();
                return request;
            },
            'requestError': function(rejection) {
            	console.log('requestError')
            	serverMonitoring.stopToWait();
                return $q.reject(rejection);
            },
            'response': function(response) {
            	console.log('response')
            	serverMonitoring.stopToWait();
                return response;  
            },
            'responseError': function(rejection) {
            	console.log('responseError')
                serverMonitoring.stopToWait();
            	loc =$location.path()
                serverMonitoring.signalError();
                return $q.reject(rejection);
            }
        }
    });
}]);
