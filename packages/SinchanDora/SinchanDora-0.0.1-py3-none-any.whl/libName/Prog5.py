def prog5():
    print(" 

<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js">
    </script>
    <script>
        var app= angular.module("studentDetail",[]);
        app.controller("studentDetailCntrl",function($scope){
            $scope.studata=[]

            $scope.generateData=function(){
                $scope.studata=[]
                for (var  i=1; i <= $scope.num;i++){
                    var stud={
                        "SLNO":i,
                        "NAME":'Student-'+i,
                        "CGPA":(Math.random()*10).toFixed(2)

                    }
                    $scope.studata.push(stud)
                }
            }
        });
    </script>
</head>

<body ng-app="studentDetail">
    <h1>Student Detail Aplication</h1>
    <div ng-controller="studentDetailCntrl">
        Enter the Number Of student to generateData:
        <input type="number" ng-model="num">
        <button ng-click="generateData()">Generate</button>

        <br/>
        <table border="1" ng-show="studata.length>0">
            <tr>
                <th>SLNO</th>
                <th>NAME</th>
                <th>CGPA</th>
            </tr>
            <tr ng-repeat="student in studata">

                <td>{{student.SLNO}}</td>
                <td>{{student.NAME}}</td>
                <td>{{student.CGPA}}</td>
            </tr>
        </table>
        <br/>
        Number of student ={{studata.length}}
    </div>
    
</body>
</html>

")