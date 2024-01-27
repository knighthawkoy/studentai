import 'package:flutter/material.dart';

class LoggedInForm extends StatelessWidget {
  final String? isValid;
  final String? token;
  final String? modelId;
  final VoidCallback onLogout;

  const LoggedInForm({
    Key? key,
    required this.isValid,
    required this.token,
    required this.modelId,
    required this.onLogout,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Text('Welcome!', style: TextStyle(fontSize: 24)),
        Text('Is Valid: $isValid'),
        Text('Token: $token'),
        Text('Model ID: $modelId'),
        ElevatedButton(
          onPressed: onLogout,
          child: Text('Logout'),
        ),
      ],
    );
  }
}
