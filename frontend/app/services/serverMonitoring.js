mainApplication.factory("serverMonitoring", ['$rootScope',function($rootScope) {
    return {
        startToWait : function() {
            $rootScope.$broadcast("waitingServerStart",true);
        },
        stopToWait : function() {
            $rootScope.$broadcast("waitingServerStop",false);
        },
        signalError : function() {
            $rootScope.$broadcast("errorServerDetected",false);
        }
    };
}]);
