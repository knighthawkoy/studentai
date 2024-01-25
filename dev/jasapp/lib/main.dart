import 'package:flutter/material.dart';
import 'package:pocketbase/pocketbase.dart';
import 'package:jasapp/views/login_form.dart';

final pb = PocketBase('http://192.168.68.20:9220');

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: LoginForm(pb: pb),
      ),
    );
  }
}