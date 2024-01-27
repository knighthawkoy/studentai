import 'package:flutter/material.dart';
import 'package:pocketbase/pocketbase.dart'; // Import PocketBase
import 'logged_in_form.dart'; // Import LoggedInForm

class LoginForm extends StatefulWidget {
  final PocketBase pb; // Add this line

  const LoginForm({Key? key, required this.pb}) : super(key: key);

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
        var authData = await widget.pb.admins.authWithPassword(
          _emailController.text.trim(),
          _passwordController.text.trim(),
        );
        setState(() {
          isValid = widget.pb.authStore?.isValid?.toString() ?? 'Unknown';
          token = widget.pb.authStore?.token ?? 'Unknown';
          modelId = widget.pb.authStore?.model?.id ?? 'Unknown';
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
      return LoggedInForm(
        isValid: isValid,
        token: token,
        modelId: modelId,
        onLogout: () {
          setState(() {
            isLoggedIn = false;
            isValid = null;
            token = null;
            modelId = null;
          });
        },
      );
    } else {
      return Form(
        key: _formKey,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center, // Add this line
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
}