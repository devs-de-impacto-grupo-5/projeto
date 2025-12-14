import { useState } from 'react';
import AssistenteMessage from '../AssistenteMessage';
import ProdutorMessage from '../ProdutorMessage';
import ChatHeader from '../ChatHeader';
import ChatInput from '../ChatInput';
import ChatOptions from '../ChatOptions';
import FileUpload from '../FileUpload';
import { Container, ChatBody, MessagesContainer, InputWrapper } from './style';

const Chat = ({
  onBack,
  onHelp,
  initialMessages,
  onSend,
  inputType,
  placeholder,
  onOptionSelect,
  showInput = true,
  showFileUpload = false,
  onFileUpload
}) => {
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

  const handleOptionSelect = (value) => {
    if (onOptionSelect) {
      onOptionSelect(value, setMessages);
    }
  };

  const handleFileUpload = (file) => {
    if (onFileUpload) {
      onFileUpload(file, setMessages);
    }
  };

  return (
    <Container>
      <ChatHeader onBack={onBack} onHelp={onHelp} />
      <ChatBody>
        <MessagesContainer>
          {messages.map((msg, index) =>
            msg.type === 'assistente' ? (
              <AssistenteMessage key={index}>{msg.text}</AssistenteMessage>
            ) : msg.type === 'options' ? (
              <ChatOptions key={index} options={msg.options} onSelect={handleOptionSelect} />
            ) : (
              <ProdutorMessage key={index}>{msg.text}</ProdutorMessage>
            )
          )}
        </MessagesContainer>
      </ChatBody>

      {showFileUpload && (
        <InputWrapper>
          <FileUpload onFileSelect={handleFileUpload} />
        </InputWrapper>
      )}

      {showInput && !showFileUpload && (
        <InputWrapper>
          <ChatInput type={inputType} placeholder={placeholder} onSend={handleSend} />
        </InputWrapper>
      )}
    </Container>
  );
};

export default Chat;
