configurationController = mainController.controller('configurationController', [ '$scope', '$rootScope','$timeout','dombox', function ($scope, $rootScope, $timeout, dombox) {
    /*
    $scope.conf = {
        tempMaxThresholdOpen: 50,
        tempMinThresholdOpen: 20,
        tempMaxThresholdClose: 25,
        tempMinThresholdClose:-20,
        roofOpenHour:7,
        roofOpenMinute:30,
        roofCloseHour:20,
        roofCloseMinute:30,
        kitchenOpenHour:7,
        kitchenOpenMinute:30,
        kitchenCloseHour:20,
        kitchenCloseMinute:30,
        bathroomOpenHour:7,
        bathroomOpenMinute:30,
        bathroomCloseHour:20,
        bathroomCloseMinute:30,
        bedroomOpenHour:7,
        bedroomOpenMinute:30,
        bedroomCloseHour:20,
        bedroomCloseMinute:30,
        livingRoomEastOpenHour:7,
        livingRoomEastOpenMinute:30,
        livingRoomEastCloseHour:20,
        livingRoomEastCloseMinute:30,
        livingRoomWestOpenHour:7,
        livingRoomWestOpenMinute:30,
        livingRoomWestCloseHour:20,
        livingRoomWestCloseMinute:30,
        airingRoomStartHour:19,
        airingRoomStartMinute:00,
        airingRoomStopHour:20,
        airingRoomStopMinute:00,
        alarmHour:7,
        alarmMinute:00,
        timeControlShutter:true,
        timeControlAiring:true,
        tempControlShutter:true,
        measureEnabled:true,
        alarm:true,
        delayMeasure:900,
        maxSamples:900*2,
        maxDailySamplesADay:2,
        maxDailySamples:700,
        logLevel:"INFO"
    };*/
    
    $scope.downloadConf = function() {
        dombox.getConfig().then(function(r) { $scope.conf = r.data; console.log(r); },function(r) { console.log(r); });
    };
    $scope.downloadConf();
    $scope.applyConfig = function() {
        dombox.applyConfig($scope.conf).then(function(r) { console.log("success"); },function(r) { console.log(r); });
    };
    $scope.clearLog = function() {
        dombox.clearLog().then(function(r) { console.log("success"); },function(r) { console.log(r); });
    };
}]);
