def prog1():
    print("<!DOCTYPE html>
<html ng-app="myApp">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <script
      type="text/javascript"
      src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"
    ></script>
    <script>
      var app = angular.module("myApp", []);
      app.controller("myCntrl", function ($scope) {
        $scope.firstName = "Abhishek";
        $scope.middleName = "";
        $scope.lastName = "Kumar";
        $scope.date = "mydate";
      });
    </script>
  </head>
  <body ng-app="myApp" style="background-color: gold">
    <h2>Angular JS Application to Display Full Name</h2>
    <div ng-controller="myCntrl">
      Enter First Name: <input type="text" ng-model="firstName" /><br /><br />
      Enter Middle Name: <input type="text" ng-model="middleName" /><br /><br />
      Enter Last Name: <input type="text" ng-model="lastName" /><br /><br />
      Date:<input type="date" ng-model="mydate" /><br /><br />
      Full Name : {{firstName + " " + middleName + " " + lastName}}
      <!-- Date : {Date} -->
    </div>
  </body>
</html>
")