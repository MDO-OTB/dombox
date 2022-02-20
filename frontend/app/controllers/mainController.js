mainController = mainApplication.controller('mainController', [ '$scope', '$location', function ($scope,  $location) {
	$scope.waitingServer = false;
	$scope.errorServer = false;   

    $scope.knownMenu= {
		no:-1,
		welcome:0,
        log:1,
		data:2,
		shuttle:3,
        airing:4,
		configuration:5
	};
    $scope.menu = $scope.knownMenu.no;

	$scope.selectWelcome = function() {
		$scope.menu=$scope.knownMenu.welcome;
		$location.path("/Welcome");
		console.log($location.path())
	};
    
	$scope.selectLog = function() {
		$scope.menu=$scope.knownMenu.log;
		$location.path("/Log");
		console.log($location.path())            
	};
    
	$scope.selectData = function() {
		$scope.menu=$scope.knownMenu.data;
		$location.path("/Data");
		console.log($location.path())            
	};

    $scope.selectShuttle = function() {
		$scope.menu=$scope.knownMenu.shuttle;
		$location.path("/Shutter");
		console.log($location.path())
	};

    $scope.selectAiring = function() {
		$scope.menu=$scope.knownMenu.airing;
		$location.path("/Airing");
		console.log($location.path())
	};
    
    $scope.selectConfiguration = function() {
		$scope.menu=$scope.knownMenu.configuration;
		$location.path("/Configuration");
		console.log($location.path())
	};
    
	resetMenuNav = function() {
		$scope.menu=$scope.knownMenu.no;
	};
        
    $scope.$on("waitingServerStart", function(evt,data) {
		$scope.waitingServer = true; 
	});
	$scope.$on("waitingServerStop", function(evt,data) {
		$scope.waitingServer = false;   
		$scope.errorServer = false;   
	});

	$scope.$on("errorServerDetected", function(evt,data) {
		$scope.waitingServer = false;   
		$scope.errorServer = true;   
	});

	handleF5 = function(url){
                console.log("handleF5");
		switch(url) {
			case '/Welcome':
				$scope.selectWelcome();
				break;
			case '/Log':
				$scope.selectLog();
				break;
			case '/Data':
				$scope.selectData();
				break;
			case '/Shuttle':
				$scope.selectShuttle();
				break;
			case '/Airing':
				$scope.selectAiring();
				break;
			case '/Configuration':
				$scope.selectConfiguration();
				break;
		} 
	};

	resetMenuNav();
	if($scope.page == undefined) {
		handleF5($location.url());
	}
}]);
