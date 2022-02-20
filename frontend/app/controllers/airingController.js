mainController.controller("airingController", ['$scope','$rootScope', '$timeout','dombox', function ($scope,$rootScope, $timeout, dombox) {  
    $scope.airingRoofStart = function() {
        $scope.controlAiring('start');
    };
    $scope.airingRoofStop = function() {
        $scope.controlAiring('stop');
    };
    $scope.controlAiring = function(action) {
        dombox.controlAiring(action,'bedroom').then(function(r) { },function(r) { console.log(r); });
    };
}]);
