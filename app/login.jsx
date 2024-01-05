import React from 'react';
import { Button, Alert } from 'react-native';
import axios from 'axios';

export default class App extends React.Component {
  login = async () => {
    try {
      const response = await axios.post('http://your_server_ip:5000/v1/account/login', {
        username: 'username',
        password: 'password'
      });
      Alert.alert('Token:', response.data.token);
    } catch (error) {
      Alert.alert('Login failed:', error.toString());
    }
  };

  render() {
    return <Button title="Login" onPress={this.login} />;
  }
}