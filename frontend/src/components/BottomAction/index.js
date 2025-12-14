import { FiArrowRight } from 'react-icons/fi';
import { Container, Button, ButtonText, Description } from './style';

const BottomAction = ({ buttonText, description, onClick, disabled = false }) => {
  return (
    <Container>
      <Button onClick={onClick} disabled={disabled}>
        <ButtonText>{buttonText}</ButtonText>
        <FiArrowRight size={20} />
      </Button>
      {description && <Description>{description}</Description>}
    </Container>
  );
};

export default BottomAction;
