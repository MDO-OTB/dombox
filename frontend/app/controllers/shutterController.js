mainController.controller("shuttleController", ['$scope','$rootScope', '$timeout','dombox', function ($scope,$rootScope, $timeout, dombox) {  
    $scope.shutterRoof ='bedroom_remi';
    $scope.shutterStage ='bedroom_parents';
    $scope.shutterStatus = '';
    $scope.shutterStatusReceived = false;
    $scope.shutterRoofOpen = function() {
        $scope.controlRoofShutter('open');
    };
    $scope.shutterRoofStop = function() {
        $scope.controlRoofShutter('stop');
    };
    $scope.shutterRoofClose = function() {
        $scope.controlRoofShutter('close');
    };
    $scope.shutterRoofForceOpen = function() {
        $scope.controlRoofShutter('force_open');
    };
    $scope.shutterRoofForceClose = function() {
        $scope.controlRoofShutter('force_close');
    };
    $scope.shutterStageOpen = function() {
        $scope.controlStageShutter('open');
    };
    $scope.shutterStageStop = function() {
        $scope.controlStageShutter('stop');
    };
    $scope.shutterStageClose = function() {
        $scope.controlStageShutter('close');
    };
    $scope.shutterHouseOpen = function() {
        $scope.controlHouseShutter('open');
    };
    $scope.shutterHouseClose = function() {
        $scope.controlHouseShutter('close');
    };
    timeoutForRefresh1=2000;
    timeoutForRefresh2=35000;    
    $scope.controlRoofShutter = function(action) {
        dombox.controlShutter(action,$scope.shutterRoof).then(function(r) {
            console.log("success");
            $timeout($scope.refreshShutterStatus, timeoutForRefresh1);
            $timeout($scope.refreshShutterStatus, timeoutForRefresh2);
        },function(r) {
            console.log(r)
        });
    };

    $scope.controlStageShutter = function(action) {
        dombox.controlShutter(action,$scope.shutterStage).then(function(r) {
            console.log("success");
        },function(r) {
            console.log(r);
        });
    };
    $scope.controlHouseShutter = function(action) {
        dombox.controlShutter(action,'house').then(function(r) {
            console.log("success");
        },function(r) {
            console.log(r);
        });
    };
    processStatus = function(r) {
        console.log(r);
        $scope.shutterStatusReceived = true;
        switch(r.data) {
            case 'opened':
                $scope.shutterStatus='Ouvert'
                break;
            case 'opening':
                $scope.shutterStatus='Ouverture en cours'
                break;
            case 'closed':
                $scope.shutterStatus='Fermé'
                break;
            case 'closing':
                $scope.shutterStatus='Fermeture en cours'
                break;
            case 'unknown':
                $scope.shutterStatus='Inconnu'
                break;
        } 
    };
    
    $scope.refreshShutterStatus = function() {
        $scope.shutterStatusReceived = false;
        dombox.getShutterStatus($scope.shutterRoof).then(processStatus,function(r) {
            console.log(r);
        });
    };
    $scope.refreshShutterStatus();

}]);
