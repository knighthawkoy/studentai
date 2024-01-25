
import 'package:flutter/material.dart';
import 'package:pocketbase/pocketbase.dart';

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
      body: LoginForm(),
      ),
    );
  }
}

class LoginForm extends StatefulWidget {
  const LoginForm({Key? key}) : super(key: key);

  @override
  LoginFormState createState() => LoginFormState();
}

class LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  // Define your variables here
  String? isValid;
  String? token;
  String? modelId;

  Future<void> _authenticateUser() async {
    if (_formKey.currentState?.validate() ?? false) {
      try {
        var authData = await pb.admins.authWithPassword(
          _emailController.text.trim(),
          _passwordController.text.trim(),
        );
        setState(() {
          isValid = pb.authStore?.isValid?.toString() ?? 'Unknown';
          token = pb.authStore?.token ?? 'Unknown';
          modelId = pb.authStore?.model?.id ?? 'Unknown';
        });
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('An error occurred: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: <Widget>[
          TextFormField(
            controller: _emailController,
            validator: (String? value) {
              if (value == null || value.isEmpty) {
                return 'Please enter your email';
              } else if (!value.contains('@')) {
                return 'Please enter a valid email';
              }
              return null;
            },
          ),
          TextFormField(
            controller: _passwordController,
            validator: (String? value) {
              if (value == null || value.isEmpty) {
                return 'Please enter your password';
              }
              return null;
            },
          ),
          ElevatedButton(
            onPressed: _authenticateUser,
            child: const Text('Sign In'),
          ),
          Text('Is Valid: $isValid'),
          Text('Token: $token'),
          Text('Model ID: $modelId'),
        ],
      ),
    );
  }
}