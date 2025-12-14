import { Container, IconWrapper, MessageBox, MessageText } from './style';
import { ReactComponent as ProdutorIcon } from '../../assets/svgs/produtor.svg';

const ProdutorMessage = ({ children }) => {
  return (
    <Container>
      <MessageBox>
        <MessageText>{children}</MessageText>
      </MessageBox>
      <IconWrapper>
        <ProdutorIcon width={48} height={48} />
      </IconWrapper>
    </Container>
  );
};

export default ProdutorMessage;
