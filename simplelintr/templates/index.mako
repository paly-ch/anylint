<html ng-app="SimpleLintr">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="static/css/bootstrap.css"  type="text/css"/>
    <link href="static/css/admin.css" rel="stylesheet">
    <link href="static/css/lintr.css" rel="stylesheet">

    <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/0.9.16/socket.io.min.js"></script>

    <script src="static/js/jquery-1.11.0.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>

    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.2.16/angular.js"></script>
    <script src="static/js/app.js"></script>

    <title>Simple Lintr</title>
</head>
<body>

<div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
  <div class="container-fluid">
    <div class="navbar-header">
      <span class="navbar-brand docker-title">Simple Lintr</span>
    </div>
  </div>
</div>

<div class="container-fluid" ng-controller="SidebarController">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
            <li ng-repeat="sidebar in sidebars"><a href="javascript:void(0);" ng-click="sidebar.visible = !sidebar.visible">{{sidebar.name}}</a>
                <ul class="nav nav-sidebar" ng-if="sidebar.visible" style="padding-left: 40px;">
                    <li ng-repeat="option in sidebar.options" ng-class="{active: selectedOption == option}">
                        <a href="javascript:void(0);" ng-click="setSelectedOption(option)">{{option.name}}</a>
                    </li>
                </ul>
            </li>
          </ul>
        </div>
      </div>

      <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h1 class="page-header" style="color: {{ dockerColour }}">Status: {{ dockerStatus }}</h1>
          <div ng-include="selectedOption.url"></div>
      </div>
</div>
<div id="screenshadow"><div id="terminalwindow"></div></div>
</body>
</html>
