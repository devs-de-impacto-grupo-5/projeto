import { useState } from 'react';
import AssistenteMessage from '../AssistenteMessage';
import ProdutorMessage from '../ProdutorMessage';
import ChatHeader from '../ChatHeader';
import ChatInput from '../ChatInput';
import { Container, MessagesContainer } from './style';

const Chat = ({ onBack, onHelp, initialMessages, onSend, inputType, placeholder }) => {
  const [messages, setMessages] = useState(initialMessages || []);

  const handleSend = (message) => {
    // Adiciona mensagem do produtor (censura se for senha)
    const displayText = inputType === 'password' ? '•'.repeat(message.length) : message;
    setMessages(prev => [...prev, { type: 'produtor', text: displayText }]);

    // Chama callback externo se fornecido (passa a mensagem original)
    if (onSend) {
      onSend(message, setMessages);
    }
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
        type={inputType}
        placeholder={placeholder}
        onSend={handleSend}
      />
    </Container>
  );
};

export default Chat;
