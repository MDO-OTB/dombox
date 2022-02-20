topController = mainController.controller('topController', [ '$scope', '$rootScope', '$timeout','dombox', function ($scope, $rootScope,$timeout,dombox) {
    timeoutForRefresh=300000;
    $scope.front_version = '0.0.2';

    processSuccess = function(r) {    
        $scope.back_version = r.data[0];
        $scope.host_name = r.data[1];
        $scope.host_ip = r.data[2];
        $scope.host_uptime = r.data[3];
        $timeout($scope.refreshTopBar, timeoutForRefresh);
    };
    
    $scope.refreshTopBar = function() {
        dombox.getTop().then(processSuccess,function(r) {
            $timeout($scope.refreshTopBar, timeoutForRefresh);
        });
    };
    $scope.refreshTopBar();

}]);
