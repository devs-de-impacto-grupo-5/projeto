import Chat from '../../components/Chat';

const Login = () => {
  return (
    <Chat
      onBack={() => console.log('Back')}
      onHelp={() => console.log('Help')}
    />
  );
};

export default Login;
