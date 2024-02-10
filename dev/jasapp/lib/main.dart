import 'package:flutter/material.dart';
import 'package:pocketbase/pocketbase.dart';
import 'package:jasapp/views/login_form.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart' as dotenv;

final pb = PocketBase('http://192.168.68.20:9220');

void main() async {
  await dotenv.dotenv.load();
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
// Additional imports:
import 'package:flutter/foundation.dart';

void verifyApp() {
  final isDebug = kDebugMode;
  final serverAddress = pb.client.baseUrl;

  debugPrint('App is in debug mode: $isDebug');
  debugPrint('PocketBase server address: $serverAddress');
}

@override
void initState() {
  super.initState();
  verifyApp();
}}
