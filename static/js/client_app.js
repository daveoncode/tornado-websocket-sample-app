angular.module('app', []).
    controller('TokenFormController', function($scope) {
        'use strict';

        var debug = document.getElementById('debug-console');

        $scope.shouldDisplayErrorMessage = function() {
            return $scope.invalidToken || ($scope.invalidSubmit && $scope.tokenForm.token.$invalid);
        };

        $scope.validateToken = function() {
            if ($scope.tokenForm.$invalid) {
                $scope.invalidSubmit = true;
            }
            else {
                $scope.invalidSubmit = false;

                var socketURL = 'ws://' + location.host + '/ws/client/?token=' + $scope.token;
                var socket = new WebSocket(socketURL);

                socket.onopen = function(event) {
                    debug.innerHTML += '> WebSocket client connection opened (url: ' + socketURL + ')<br />';
                };

                socket.onmessage = function(message) {
                    debug.innerHTML += '> Message received from server: ' + message.data + '<br />';
                    if (String(message.data) === String($scope.token)) {
                        debug.innerHTML += '> Token confirmed!<br />';
                        //var body = document.getElementsByTagName('body')[0];
                        var gestureManager = new Hammer(document.body, {prevent_default: true});

                        gestureManager.get('pinch').set({ enable: true });

                        gestureManager.on('swipeleft', function() {
                            debug.innerHTML += '> Sending SWIPE_LEFT gesture<br/>';
                            socket.send('SWIPE_LEFT');
                        });

                        gestureManager.on('swiperight', function() {
                            debug.innerHTML += '> Sending SWIPE_RIGHT gesture<br/>';
                            socket.send('SWIPE_RIGHT');
                        });

                        gestureManager.on('tap', function() {
                            debug.innerHTML += '> Sending TAP gesture<br/>';
                            socket.send('TAP');
                        });

                        gestureManager.on('doubletap', function() {
                            debug.innerHTML += '> Sending DOUBLE_TAP gesture<br/>';
                            socket.send('DOUBLE_TAP');
                        });

                        $scope.$apply(function() {
                            $scope.$parent.tokenAccepted = true;
                        });
                    }
                };

                socket.onclose = function(event) {
                    debug.innerHTML += '> WebSocket connection closed<br />';
                    if (event.code === 401) {
                        $scope.$apply(function() {
                            $scope.invalidToken = true;
                            $scope.tokenForm.$setValidity('token', false);
                        });
                    }
                };

                socket.onerror = function(error) {
                    debug.innerHTML += '> Error: <br />';
                    for (var i in error) {
                        debug.innerHTML += i;
                        debug.innerHTML += ': ';
                        debug.innerHTML += error[i] + '<br />';
                    }
                    console.log('WebSocket Error ' + error);
                };

            }
        };
    });
