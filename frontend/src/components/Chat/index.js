import { useState } from 'react';
import AssistenteMessage from '../AssistenteMessage';
import ProdutorMessage from '../ProdutorMessage';
import ChatHeader from '../ChatHeader';
import ChatInput from '../ChatInput';
import { Container, MessagesContainer } from './style';

const Chat = ({ onBack, onHelp }) => {
  const [messages, setMessages] = useState([
    { type: 'assistente', text: 'Olá! Seja bem-vindo(a) ao Vitalis! \n \n Por favor, para sua segurança, digite seu CPF.' }
  ]);

  const handleSend = (message) => {
    setMessages([...messages, { type: 'produtor', text: message }]);
  };

  return (
    <Container>
      <ChatHeader onBack={onBack} onHelp={onHelp} />
      <MessagesContainer>
        {messages.map((msg, index) => (
          msg.type === 'assistente' ? (
            <AssistenteMessage key={index}>{msg.text}</AssistenteMessage>
          ) : (
            <ProdutorMessage key={index}>{msg.text}</ProdutorMessage>
          )
        ))}
      </MessagesContainer>
      <ChatInput
        placeholder="Digite seu CPF aqui"
        onSend={handleSend}
      />
    </Container>
  );
};

export default Chat;
