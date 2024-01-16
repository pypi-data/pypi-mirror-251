def prog2():
    print("<!DOCTYPE html>
<html ng-app="myApp">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Shopping list Application</title>
  </head>
  <script
    type="text/javascript"
    src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"
  ></script>
  <script>
    var app = angular.module("myApp", []);
    app.controller("myCntrl", function ($scope) {
      $scope.ShoppingItems = ["a", "b"];
      $scope.addItem = function () {
        if (
          $scope.newItem &&
          $scope.ShoppingItems.indexOf($scope.newItem) == -1
        ) {
          $scope.ShoppingItems.push($scope.newItem);
          $scope.newItem = "";
        } else {
          if ($scope.newItem) {
            alert("This items is already in the shopping list");
            alert("Please enter the item to be add");
          }
        }
      };

      $scope.removeItem = function () {
        if ($scope.ShoppingItems.indexOf($scope.selectItem) == -1) {
          alert("please select items to remove");
        } else {
          var index = $scope.ShoppingItems.indexOf($scope.selectItem);
          $scope.ShoppingItems.splice(index, 2);
          $scope.selectItem = "";
        }
      };
    });
  </script>
  <body style="background-color: yellow">
    <div ng-controller="myCntrl">
      <h2>Shopping Application</h2>
      <h4>list of shopping items</h4>
      <table border="1">
        <tr>
          <th>SlNo</th>
          <th>Items</th>
        </tr>

        <tr ng-repeat="items in ShoppingItems">
          <td>{{$index+1}}</td>
          <td>{{items}}</td>
        </tr>
      </table>
      <br />
      <div>
        Enter the Item to Add : <input type="text" ng-model="newItem" />
        <button ng-click="addItem()">Add Items</button>
        Enter the Item to Remove :
        <select
          ng-model="selectItem"
          ng-options="item for item in ShoppingItems"
        ></select>
        <button ng-click="removeItem()">removeItem</button>
      </div>
    </div>
  </body>
</html>
")