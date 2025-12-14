import { useState } from 'react';
import { FiSend } from 'react-icons/fi';
import { Container, Input, SendButton } from './style';

const ChatInput = ({ placeholder = 'Digite aqui', type = 'text', onSend }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSend(message);
      setMessage('');
    }
  };

  return (
    <Container onSubmit={handleSubmit}>
      <Input
        type={type}
        placeholder={placeholder}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <SendButton type="submit">
        <FiSend size={20} />
      </SendButton>
    </Container>
  );
};

export default ChatInput;
