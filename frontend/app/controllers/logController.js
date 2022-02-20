logController = mainController.controller('logController', [ '$scope', '$rootScope', '$timeout','dombox', function ($scope, $rootScope,$timeout,dombox) {
    timeoutForRefresh=300000;
    $scope.receivedLog='';

    processSuccess = function(r) {
        $scope.receivedLog=r.data;
        $timeout($scope.refreshLog, timeoutForRefresh);
    };
    
    $scope.refreshLog = function() {
        dombox.getLog().then(processSuccess,function(r) {
            $timeout($scope.refreshLog, timeoutForRefresh);
        });
    };
    $scope.refreshLog();
}]);
