mainController.controller("dataController", ['$scope','$rootScope', '$timeout','dombox', function ($scope,$rootScope, $timeout, dombox) {
  $scope.graphPrint = false;
  $scope.what = 'temperature';
  $scope.step = 'hour';
  $scope.printTempAM2302_1 = false;
  $scope.printTempAM2302_2 = false;
  $scope.printTempBMP085 = true;

  $scope.printHumiAM2302_1 = false;
  $scope.printHumiAM2302_2 = false;
  $scope.printPresBMP085 = true;

  $scope.printShutter1 = true;
  $scope.printShutter2 = true;

  data = null;
  clearGraph = function() {
    $scope.graphLinePrint = false;
      delete $scope.data;
      delete $scope.labels;
      delete $scope.series;
      $scope.data = [];
      $scope.labels = [];
      $scope.series = [];
  };
  
  $scope.updateGraph = function() {
        clearGraph();
        switch($scope.what) {
        	case 'temperature':
                    $scope.graphTitle = "Temperature (°C)";
                    if($scope.printTempAM2302_1) {
                        $scope.data.push(data[1])
                        $scope.series.push("AM2302_1")
                    }
                    if($scope.printTempAM2302_2) {
                        $scope.data.push(data[2])
                        $scope.series.push("AM2302_2")
                    }
                    if ($scope.printTempBMP085) {
                        $scope.data.push(data[3])
                        $scope.series.push("BMP085")
                    }
                    break;
        	case 'humidity':
                    $scope.graphTitle = "Humidité (%)";                 
                    if($scope.printHumiAM2302_1) {
                        $scope.data.push(data[1])
                        $scope.series.push("AM2302_1")
                    }
                    if($scope.printHumiAM2302_2) {
                        $scope.data.push(data[2])
                        $scope.series.push("AM2302_2")
                    }
                    break;
        	case 'pressure':
                    $scope.graphTitle = "Préssion atmosphérique (PA)";
                    if($scope.printPresBMP085) {
                        $scope.data.push(data[1])
                        $scope.series.push("BMP085")
                    }
                    
                    break;
        	case 'shutter':
                    $scope.graphTitle = "Volet";
                    if($scope.printShutter1) {
                        $scope.data.push(data[1])
                        $scope.series.push("Volet Camille")
                    }
                    if ($scope.printShutter2) {
                        $scope.data.push(data[2])
                        $scope.series.push("Volet Rémi")
                    }
                    break;
        }
        angular.forEach(data[0], function(value, key) {
            d = new Date(0);
            d.setUTCSeconds(value);
            switch($scope.step) {
            case 'hour':
                $scope.labels[key] = d.getHours() + ':' + d.getMinutes();
                break;
            case 'day':
                $scope.labels[key] = d.getDate() + ' - ' + d.getHours() + ':' + d.getMinutes();
                break;
            }
        });
        switch($scope.step) {
            case 'hour':
                $scope.graphLinePrint = true;
                $scope.graphBarPrint = false;
                break;
            case 'day':
                $scope.graphLinePrint = false;
                $scope.graphBarPrint = true;
                break;
        }
    };
      
  $scope.downloadData = function() {
      $scope.graphLinePrint = false;
        dombox.getData($scope.what,$scope.step).then(function(r) {
            clearGraph();
            data = r.data;
            $scope.updateGraph();
        },function(r) {
          console.log(r);
      });
  };
  $scope.downloadData();  
}]);
