import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

class ExploreScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MyApp1();
  }
}

class MyApp1 extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text('Explore Catches Nearby!')), body: GeolocationExample());
  }
}

class GeolocationExampleState extends State {
  Geolocator _geolocator;
  Position _position;
  double _positionLatitude = 34.3;
  GoogleMapController mapController;
  double _positionLongitude = 32.3;

  final apiKey = "AIzaSyCILGP87TZPkXUobQfqDp9mkPA7IXnEGXU";
  void checkPermission() {
    _geolocator.checkGeolocationPermissionStatus().then((status) {
      print('status: $status');
    });
    _geolocator
        .checkGeolocationPermissionStatus(
            locationPermission: GeolocationPermission.locationAlways)
        .then((status) {
      print('always status: $status');
    });
    _geolocator.checkGeolocationPermissionStatus(
        locationPermission: GeolocationPermission.locationWhenInUse)
      ..then((status) {
        print('whenInUse status: $status');
      });
  }

Future<void> _gotoLocation(double lat, double long) async {
    mapController.animateCamera(CameraUpdate.newCameraPosition(CameraPosition(
      target: LatLng(lat, long),
      zoom: 20,
      tilt: 50.0,
      bearing: 45.0,
    )));
  }

  void updateLocation() async {
    try {
      Position newPosition = await Geolocator()
          .getCurrentPosition(desiredAccuracy: LocationAccuracy.high)
          .timeout(new Duration(seconds: 10));
      setState(() {
        _position = newPosition;
        _positionLatitude = _position.latitude;
        _positionLongitude = _position.longitude;
        print(_positionLatitude);
        print(_positionLongitude);
        _gotoLocation(_positionLatitude,_positionLongitude);
      });
    } catch (e) {
      print('Error: ${e.toString()}');
    }
  }

  @override
  void initState() {
    super.initState();
    _geolocator = Geolocator();
    updateLocation();
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: (_positionLatitude != null)
          ? Container(
              child: Column(
                children: <Widget>[
                  Stack(
                    children: <Widget>[
                      Container(
                        height: MediaQuery.of(context).size.height,
                        width: MediaQuery.of(context).size.width,
                        child: GoogleMap(
                            initialCameraPosition: CameraPosition(
                                target: LatLng(
                                    _positionLatitude, _positionLongitude),
                                zoom: 7.0),
                            onMapCreated: (GoogleMapController controller) {
                              mapController = controller;
                            },
                            zoomGesturesEnabled: true,
                            myLocationButtonEnabled: false,
                            myLocationEnabled: true,
                            compassEnabled: false,
                            mapToolbarEnabled: true,
                            circles: Set.from([
                              Circle(
                                  circleId: CircleId('0'),
                                  center: LatLng(
                                      _positionLatitude, _positionLongitude),
                                  radius: 1250,
                                  strokeColor: Color(0x5DA9CAff),
                                  strokeWidth: 1,
                                  fillColor: Color(0x5DA9CAff)),
                              Circle(
                                  circleId: CircleId('1'),
                                  center: LatLng(
                                      _positionLatitude, _positionLongitude),
                                  radius: 2500,
                                  strokeColor: Color(0x3DA9CAff),
                                  strokeWidth: 1,
                                  fillColor: Color(0x3DA9CAff)),
                              Circle(
                                  circleId: CircleId('2'),
                                  center: LatLng(
                                      _positionLatitude, _positionLongitude),
                                  radius: 5000,
                                  strokeColor: Color(0x2DA9CAff),
                                  strokeWidth: 1,
                                  fillColor: Color(0x2DA9CAff))
                            ])),
                      ),
                    ],
                  ),
                ],
              ),
            )
          : Center(
              child: CircularProgressIndicator(),
            ),
    );
  }
}

class GeolocationExample extends StatefulWidget {
  @override
  GeolocationExampleState createState() => new GeolocationExampleState();
}