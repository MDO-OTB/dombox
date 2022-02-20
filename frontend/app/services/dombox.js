mainApplication.factory("dombox", ['$http','serverMonitoring',function($http, serverMonitoring) {
    var baseUrlServlet  = location.origin + '/dombox_server.py';
    var paramsForRequest = null;
    return {
        getData :  function(pwhat, pstep) { 
            paramsForRequest = {what:pwhat, step:pstep};
            return $http.get(baseUrlServlet, {  params : paramsForRequest}); 
        },
        getTop : function() {
            paramsForRequest = {what:'top'};
            return $http.get(baseUrlServlet, {  params : paramsForRequest});
        },
        getLog : function() {
            paramsForRequest = {what:'log'};
            return $http.get(baseUrlServlet, {  params : paramsForRequest});
        },
        updateShutter : function(pshutter, paction) {
            paramsForRequest = {shutter:pshutter, action:paction};
            return $http.get(baseUrlServlet, {  params : paramsForRequest});
        },
        getConfig : function() {
            paramsForRequest = {what:'conf'};
            return $http.get(baseUrlServlet, {  params : paramsForRequest});
        },
        applyConfig : function(conf) {
             paramsForRequest = {what:'conf'};
             return $http.post(baseUrlServlet, conf, { params : paramsForRequest});
        },
        controlShutter : function(paction,pshutter) {
             paramsForRequest = {action:paction, shutter:pshutter};
             return $http.post(baseUrlServlet, paction, { params : paramsForRequest});
        },
        controlAiring : function(paction,where) {
             paramsForRequest = {action:paction, airing:where};
             return $http.post(baseUrlServlet, paction, { params : paramsForRequest});
        },
        getShutterStatus : function(pshutter) {
            paramsForRequest = {shutter:pshutter};
            return $http.get(baseUrlServlet, {  params : paramsForRequest});
        },
        clearLog : function() {
             paramsForRequest = {what:'log'};
             return $http.post(baseUrlServlet, 'clear',{ params : paramsForRequest});
        }
    };
}]);
