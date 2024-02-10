import 'package:flutter/material.dart';
import 'package:pocketbase/pocketbase.dart'; // Import PocketBase
import 'package:jasapp/logged_in_form.dart'; // Import LoggedInForm
import 'package:flutter_dotenv/flutter_dotenv.dart' as dotenv;
import 'package:jasapp/admin_service.dart';


var adminService = AdminService();
var authData = await adminService.createUser(
  _emailController.text.trim(),
  _passwordController.text.trim(),
);

class RegisterForm extends StatefulWidget {
  final PocketBase pb;

  RegisterForm({required this.pb});

  @override
  _RegisterFormState createState() => _RegisterFormState();
}

class _RegisterFormState extends State<RegisterForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  Future<void> _registerUser() async {
    if (_formKey.currentState?.validate() ?? false) {
      try {
        var authData = await widget.pb.admins.createUser(
          _emailController.text.trim(),
          _passwordController.text.trim(),
        );
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('User registered successfully!')),
        );
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
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
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
            SizedBox(height: 16.0),
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
              obscureText: true,
            ),
            SizedBox(height: 16.0),
            ElevatedButton(
              onPressed: _registerUser,
              child: const Text('Register'),
            ),
          ],
        ),
      ),
    );
  }
}
