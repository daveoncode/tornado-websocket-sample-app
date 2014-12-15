'use strict';

angular.module('app', ['ngRoute', 'ngResource']).
    config(function($resourceProvider, $routeProvider, $locationProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
        $locationProvider.html5Mode(false);
        var templateRoot = '/static/ng_templates/';
        $routeProvider.
            when('/zoom/:imageID', {
                templateUrl: templateRoot + 'detail.html'
            }).
            otherwise({
                templateUrl: templateRoot + 'gallery.html'
            });
    }).
    controller('HostController', function($scope, $resource, $location) {

        var debug = document.getElementById('debug-console');
        var protocol = location.protocol.indexOf('https') !== -1 ? 'wss://' : 'ws://';
        var socketURL = protocol + location.host + '/ws/host/?token=' + $scope.token;
        var socket = new WebSocket(socketURL);

        $scope.currentFocus = 0;

        $scope.move = function(direction) {
            var index = $scope.currentFocus + direction;
            var max = $scope.images.length - 1;
            if (index < 0) {
                debug.innerHTML += '> Force focus to first element<br />';
                index = 0;
            }
            else if (index > max) {
                debug.innerHTML += '> Force focus to the last element<br />';
                index = max;
            }
            debug.innerHTML += '> Moving focus on image index: ' + index + '<br />';
            $scope.currentFocus = index;
        };

        $scope.zoomIn = function() {
            var id = $scope.currentFocus;
            $location.path('/zoom/' + id);
            debug.innerHTML += '> Zoom on image: ' + id + '<br />';
        };

        $scope.zoomOut = function() {
            $location.path('/');
            debug.innerHTML += '> Zoom out (returning to the gallery)<br />';
        };

        socket.onopen = function(event) {
            debug.innerHTML += '> WebSocket host connection opened (url: ' + socketURL + ')<br />';
            debug.innerHTML += '> Waiting for mobile device connection...<br />';
        };

        socket.onmessage = function(message) {
            debug.innerHTML += '> Message received from server: ' + message.data + '<br />';
            if (String(message.data) === String($scope.token)) {
                debug.innerHTML += '> Mobile device connected!<br />';

                $scope.$apply(function() {
                    $scope.tokenAccepted = true;
                });

                debug.innerHTML += '> Calling Flickr API...<br />';

                $resource('/api/').query(function(response) {
                    $scope.images = angular.isArray(response) ? response : [];
                    debug.innerHTML += '> Data received :)<br />';
                }, function() {
                    debug.innerHTML += '> Something went wrong during the call to Flickr service :(<br />';
                });
            }
            else {
                switch (message.data) {
                    case 'SWIPE_LEFT':
                        $scope.$apply(function($scope) {
                            $scope.move(1);
                        });
                        break;
                    case 'SWIPE_RIGHT':
                        $scope.$apply(function($scope) {
                            $scope.move(-1);
                        });
                        break;
                    case 'TAP':
                        $scope.$apply(function($scope) {
                            $scope.zoomIn();
                        });
                        break;
                    case 'DOUBLE_TAP':
                        $scope.$apply(function($scope) {
                            $scope.zoomOut();
                        });
                        break;
                    default:
                        debug.innerHTML += '> Unsupported gesture :/<br />';
                }
            }
        };

        socket.onclose = function(event) {
            debug.innerHTML += '> WebSocket host connection closed<br />';
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
    });
