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
    return Stack(
      children: <Widget>[
        Align(
          alignment: Alignment.topCenter,
          child: Padding(
            padding: const EdgeInsets.only(top: 50.0),
            child: Text('Welcome!', style: TextStyle(fontSize: 24)),
          ),
        ),
        Align(
          alignment: Alignment.bottomLeft,
          child: Padding(
            padding: const EdgeInsets.only(bottom: 50.0, left: 10.0),
            child: ElevatedButton(
              onPressed: onLogout,
              child: Text('<'),
            ),
          ),
        ),
      ],
    );
  }
}
