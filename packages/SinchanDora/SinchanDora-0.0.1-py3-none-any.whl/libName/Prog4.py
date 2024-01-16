def prog4():
    print(" 

<!DOCTYPE html>
<html>
    <title>AJS SQUARE AND FACTORIAL</title>
    <head>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js">
        </script>
        <script>
            var app=angular.module("mysq",[]);
            app.controller("sqcntrl",function($scope){
                $scope.num=0
                $scope.fac=1
                $scope.sqr=0
                $scope.fact=function(){
                    $scope.fac=1
                    if($scope.num==0){
                        $scope.fac=1
                    }
                    else{
                        for(var i=$scope.num;i!=0;i--){
                        $scope.fac=$scope.fac*i
                    }

                    }
                }
                $scope.square=function(){
                    $scope.sq=$scope.num*$scope.num
                }
            });
            </script>
            </head>
            <body ng-app="mysq">
                <h1>SQUARE AND FACTORIAL</h1>
                <div ng-controller="sqcntrl">
                    ENTER THE NUMBER:<input type="number" ng-model="num">
                    <button ng-click="fact()">factorial</button>
                    <button ng-click="square()">square</button>
                    <br/><br/>
                    <b>{{"FACTORIAL OF "+ num+"="+fac}}</b>
                    <br/><br/>
                    <b>{{"SQUARE OF "+num+"="+sq}}</b>
                </div>

            </body>
</html>

 ")