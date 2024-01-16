def prog6():
    print(" 

<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js">
    </script>
    <script>
        var app =angular.module("toDoApp",[]);
        app.controller("toDoCntrl",function($scope){
            $scope.tasks =[
                {"TITLE":'TASK-1','COMPLETED':true,'EDITING':false},
                {"TITLE":'TASK-2','COMPLETED':true,'EDITING':false},
                {"TITLE":'TASK-3','COMPLETED':true,'EDITING':false}
            ]

            $scope.addTask=function(){
                if ($scope.newTask)
                {
                    var t ={
                        'TITLE':$scope.newTask,
                        'COMPLETED':false,
                        "EDITING":false
                    }

                    $scope.tasks.push(t)
                }

                else {
                    alert("pLease ENter the task to add")
                }
            }
            $scope.editTask =function(task){
                task.EDITING=true
            }
            $scope.turnOffEditing=function(task){
                task.EDITING=false
            }

            $scope.deleteTask =function(task)
            {
                var index=$scope.tasks.indexOf(task)
                $scope.tasks.splice(index,1)
            }
        });
    </script>
</head>
<body ng-app="toDoApp">
    <h1>TO DO APPILICATION</h1>
    <div ng-controller="toDoCntrl">
        Enter the name of the Task:
        <input type="text" ng-model="newTask">
        <button ng-click="addTask()">ADD TASK

        </button>
        <br/>
        <br/>
        <table border="1">
            <tr>
                <th>SlNo</th>
                <th>Status</th>
                <th>TAsk</th>
                <th>Edit</th>
                <th>Delete</th>
            </tr>
            <tr ng-repeat="task in tasks">
                <td>{{$index+1}}</td>
                <td>
                    <input type="checkbox" ng-model="task.COMPLETED">


                </td>
                <td>
                    <span ng-show="!task.EDITING">{{task.TITLE}}</span>
                    <input type="text" ng-show="task.EDITING" ng-model="task.TITLE" ng-blur="turnOffEditing(task)">
                </td>
                <td>
                    <button ng-click="editTask(task)">Edit</button>
                </td>

                <td>
                    <button ng-click="deleteTask(task)">Delete</button>
                </td>

            </tr>
        </table>
    </div>
    
</body>
</html>
")