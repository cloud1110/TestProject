'use strict';


// Declare app level module which depends on filters, and services
angular.module('xuancaiApp', ['xuancaiApp.filters', 'xuancaiApp.services', 'xuancaiApp.directives', 'xuancaiApp.controllers']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/view1', {templateUrl: 'static/partials/partial1.html', controller: 'MyCtrl1'});
    $routeProvider.when('/view2', {templateUrl: 'static/partials/partial2.html', controller: 'MyCtrl2'});
    $routeProvider.otherwise({redirectTo: '/view1'});
  }]);
