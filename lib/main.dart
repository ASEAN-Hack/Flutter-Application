import 'package:app2/Screens/Welcome/welcome_screen.dart';
import 'package:app2/constants.dart';
import 'package:flutter/material.dart';
import 'package:app2/Screens/ExploreScreen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Fisherman App',
      theme: ThemeData(
        primaryColor: kPrimaryColor,
        scaffoldBackgroundColor: Colors.white
      ),
      home: WelcomeScreen() ,
    );
  }
}
