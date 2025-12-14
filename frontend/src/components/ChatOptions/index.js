import { Container, OptionButton } from './style';

const ChatOptions = ({ options, onSelect }) => {
  return (
    <Container>
      {options.map((option, index) => (
        <OptionButton key={index} onClick={() => onSelect(option.value)}>
          {option.label}
        </OptionButton>
      ))}
    </Container>
  );
};

export default ChatOptions;
