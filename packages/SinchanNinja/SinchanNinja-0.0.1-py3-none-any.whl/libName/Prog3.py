def prog3():
    print("
<!DOCTYPE html>
<html ng-app="myApp">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple angular JS calculator</title>
    
</head>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script>
<script>
    var app =angular.module("myApp",[]);
    app.controller ("myCntrl",function($scope){
        $scope.num1=0;
        $scope.num2=1;
        $scope.result=0;
        $scope.operator="add";

        $scope.Add =function(){
            $scope.result=$scope.num1+$scope.num2
        }
        $scope.Sub =function(){
            $scope.result=$scope.num1-$scope.num2
        }
        $scope.Mul =function(){
            $scope.result=$scope.num1*$scope.num2
        }
        $scope.Div =function(){
            if ($scope.num2 == 0){
                    alert("Divide by zero")

                }
                else {
                    $scope.result = $scope.num1 / $scope.num2
                    
                } 
        }

        $scope.compute=function(){
            switch($scope.operator){
                case 'add':$scope.result=$scope.num1 + $scope.num2
                break


                case 'sub':$scope.result=$scope.num1 - $scope.num2
                break

                case 'mul':$scope.result=$scope.num1 * $scope.num2
                break

                case 'div': if ($scope.num2 == 0){
                    alert("Divide by zero")

                }
                else {
                    $scope.result = $scope.num1 / $scope.num2
                    break
                } 
            }
        }
    })
</script>
<body ng-app="myApp"> 
    <h2>Angular Js Calculator</h2>

    <div ng-controller="myCntrl">
        Enter First Number : <input type="number" ng-model="num1">
    </br>
       
        Select the operator:
            <!-- <select >
                <button ng-model="operator">+</button>
                <option ng-model="operator">*</option>
                <option ng-model="operator">-</option>
                <option ng-model="operator">/</option>
             
            </select> -->
            Enter Second  Number : <input type="number" ng-model="num2">
            <button ng-click="compute()" > Compute </button>
            <button ng-click="Add()"  value="add"> + </button>
            <button ng-click="Sub()" value="sub" > - </button>
            <button ng-click="Mul()" value="mul"> * </button>
            <button ng-click="Div()" value="div"> / </button>



            <b>{{num1 + " "+ operator+ " "+num2 +"="+result }}</b> 



    </div>
    
</body>
</html>
")