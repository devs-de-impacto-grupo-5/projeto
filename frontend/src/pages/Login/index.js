import React, { useState } from 'react';
import Forms from '../../components/Forms';
import { Container, Title, Button } from './style';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const fields = [
    {
      type: 'email',
      label: 'Email',
      placeholder: 'Digite seu email',
      value: email,
      onChange: (e) => setEmail(e.target.value),
      name: 'email',
      required: true
    },
    {
      type: 'password',
      label: 'Senha',
      placeholder: 'Digite sua senha',
      value: password,
      onChange: (e) => setPassword(e.target.value),
      name: 'password',
      required: true
    }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Login:', { email, password });
  };

  return (
    <Container>
      <Title>Login</Title>
      <form onSubmit={handleSubmit}>
        <Forms fields={fields} />
        <Button type="submit">Entrar</Button>
      </form>
    </Container>
  );
};

export default Login;
