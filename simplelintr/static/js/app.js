angular.module('docker-sidebar', []).controller('SidebarController', function($scope, $http, $timeout){
    $scope.sidebars = [
        {
            name: "Fetch",
            visible: true,
            options: [
                {
                    name: "Git",
                    url: "/static/partials/fetch/git.html"
                }
            ]
        },
        {
            name: "Containers",
            visible: true,
            options: [
                {
                    name: "View All",
                    url: "/static/partials/containers/view.html"
                },
                {
                    name: "Create",
                    url: "/static/partials/containers/create.html"
                }
            ]
        },
        {
            name: "Images",
            visible: true,
            options: [
                {
                    name: "View All",
                    url: "/static/partials/images/view.html"
                },
                {
                    name: "Build",
                    url: "/static/partials/images/build.html"
                }
            ]
        }
    ];

    $scope.selectedOption = $scope.sidebars[0].options[0];

    $scope.setSelectedOption = function(option){
        $scope.selectedOption = option;
    };

    $scope.pollingInterval = 5000;

    $scope.onPollTimeout = function(){
       $http({'method': 'GET', 'url': '/status'}).success(function(data){
           $scope.dockerStatus = data.status;
           $scope.dockerColour = data.colour;
       });

       statusPoll = $timeout($scope.onPollTimeout, $scope.pollingInterval);
    };

    var statusPoll = null;

    $scope.onPollTimeout();
});

angular.module('lintr-fetch', []).controller('FetchGitController', function($scope, $http, $timeout){
    var socket = io.connect(window.location.origin);
    socket.on('connect', function() {
        socket.emit('connected', {});
    });
    socket.on('disconnect', function() {
        hideLogWindow();
    });
    socket.removeAllListeners('log').on('log', function(msg){
        if ($('#terminalwindow').is(":hidden")) {
            showLogWindow();
        }
        $('#terminalwindow').append('<p>'+msg.log+'</p>');
        $("#terminalwindow").animate({ scrollTop: $('#terminalwindow')[0].scrollHeight}, 100);
        if (msg.status == 0) {
            setTimeout(hideLogWindow,5000);
        }
    });

    $scope.fetchGit = function(){
        var url = $('#giturl').val().trim();
        var branch = $('#branch').val().trim();
        var quiet = $('#quiet').prop('checked');
        var nocache = $('#nocache').prop('checked');
        var rm = $('#rm').prop('checked');


        socket.emit('fetchgit', {"url": url,
                              "branch": branch,
                              "quiet": quiet,
                              "nocache": nocache,
                              "rm": rm});

        // event handler for server sent data
        // the data is displayed in the "Received" section of the page
    };
});

angular.module('docker-containers', []).controller('ContainerController', function($scope, $http, $timeout){

    var pollingInterval = 5000;

    $scope.getStringForBinding = function(portBinding){
        return portBinding.Type + " : " + portBinding.IP + ":" + portBinding.PublicPort + " -> " + portBinding.PrivatePort;
    };

    var onPollTimeout = function(){
       $http({'method': 'GET', 'url': '/containers'}).success(function(data){
           $scope.containers = data.containers;
       });

       containerPoll = $timeout(onPollTimeout, pollingInterval);
    };

    var containerPoll = null;

    onPollTimeout();

    $scope.$on('$destroy', function(){
        $timeout.cancel(containerPoll);
    })
});

angular.module('docker-images', [])
.controller('ImagesController', function($scope, $http, $timeout){
    $scope.refreshImageList = function(){
        $http({'method': 'GET', 'url': '/images'}).success(function(data){
           $scope.images = data.images;
       });
    };

    $scope.refreshImageList();
})
.controller('ImageBuilderController', function($scope, $http, $timeout){
//    var socket = io.connect('http://localhost:5000');
    var socket = io.connect(window.location.origin);
    socket.on('connect', function() {
        socket.emit('Connected', {});
    });

    $scope.build = function(){
        $('#build-log').val('');

        var dir = $('#dockerfile-directory').val();
        var tag = $('#tag').val();
        var quiet = $('#quiet').prop('checked');
        var nocache = $('#nocache').prop('checked');
        var rm = $('#rm').prop('checked');

        socket.emit('build', {"dir": dir,
                              "tag": tag,
                              "quiet": quiet,
                              "nocache": nocache,
                              "rm": rm});

        // event handler for server sent data
        // the data is displayed in the "Received" section of the page
        socket.on('log', function(msg){
            $('#build-log').val($('#build-log').val() + msg.log);
            (function(){$('#build-log').scrollTop($('#build-log').height());})();
        });
    };
});

var dockerAdmin = angular.module('SimpleLintr', ['lintr-fetch', 'docker-containers', 'docker-images', 'docker-sidebar']);

var showLogWindow = function(){
    $('#terminalwindow').show();
    $('#screenshadow').show();
};
var hideLogWindow = function(){
    $('#screenshadow').hide();
    $('#terminalwindow').text("").hide();
};