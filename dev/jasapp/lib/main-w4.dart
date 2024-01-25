
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
  bool isLoggedIn = false; // Add this line

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
          isLoggedIn = true; // Set isLoggedIn to true on successful login
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

if (isLoggedIn) {
      return Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Text('Welcome!', style: TextStyle(fontSize: 24)),
          Text('Is Valid: $isValid'),
          Text('Token: $token'),
          Text('Model ID: $modelId'),
           ElevatedButton(
            onPressed: () {
              setState(() {
                isLoggedIn = false;
                isValid = null;
                token = null;
                modelId = null;
              });
            },
            child: Text('Logout')), 
        ],
      );
    }


  return Form(
    key: _formKey,
    child: Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: <Widget>[
          TextFormField(
            controller: _emailController,
            decoration: InputDecoration(
              labelText: 'Email',
              border: OutlineInputBorder(),
            ),
            validator: (String? value) {
              if (value == null || value.isEmpty) {
                return 'Please enter your email';
              } else if (!value.contains('@')) {
                return 'Please enter a valid email';
              }
              return null;
            },
          ),
          SizedBox(height: 16.0), // Add some spacing
          TextFormField(
            controller: _passwordController,
            decoration: InputDecoration(
              labelText: 'Password',
              border: OutlineInputBorder(),
            ),
            validator: (String? value) {
              if (value == null || value.isEmpty) {
                return 'Please enter your password';
              }
              return null;
            },
            obscureText: true, // Hide the password input
          ),
          SizedBox(height: 16.0), // Add some spacing
          ElevatedButton(
            onPressed: _authenticateUser,
            child: const Text('Sign In'),
            style: ElevatedButton.styleFrom(
              primary: Colors.blue, // Set the button color
              onPrimary: Colors.white, // Set the text color
            ),
          ),
        ],
      ),
    ),
  );
}
}