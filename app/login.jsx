import React from 'react';
import { Button, Alert } from 'react-native';
import axios from 'axios';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

class LoginScreen extends React.Component {
  login = async () => {
    try {
      const response = await axios.post('http://your_server_ip:5000/v1/account/login', {
        username: 'username',
        password: 'password'
      });
      Alert.alert('Token:', response.data.token);
      this.props.navigation.navigate('Home');
    } catch (error) {
      Alert.alert('Login failed:', error.toString());
    }
  };

  render() {
    return <Button title="Login" onPress={this.login} />;
  }
}

class HomeScreen extends React.Component {
  render() {
    return <Text>Welcome to Home Screen</Text>;
  }
}

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
