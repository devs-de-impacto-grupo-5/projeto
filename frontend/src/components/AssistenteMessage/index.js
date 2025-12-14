import React from 'react';
import { Container, IconWrapper, MessageBox, MessageText } from './style';
import { ReactComponent as Logo } from '../../assets/svgs/logo.svg';

const AssistenteMessage = ({ children }) => {
  return (
    <Container>
      <IconWrapper>
        <Logo width={32} height={32} />
      </IconWrapper>
      <MessageBox>
        <MessageText>{children}</MessageText>
      </MessageBox>
    </Container>
  );
};

export default AssistenteMessage;
