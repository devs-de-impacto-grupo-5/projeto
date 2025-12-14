import React from 'react';
import { Container, IconWrapper, MessageBox, MessageText, TypingIndicator, Dot } from './style';
import { ReactComponent as Logo } from '../../assets/svgs/logo.svg';

const AssistenteMessage = ({ children }) => {
  const isTyping = children === 'typing';

  return (
    <Container>
      <IconWrapper>
        <Logo width={32} height={32} />
      </IconWrapper>
      <MessageBox>
        {isTyping ? (
          <TypingIndicator>
            <Dot delay="0s" />
            <Dot delay="0.2s" />
            <Dot delay="0.4s" />
          </TypingIndicator>
        ) : (
          <MessageText>{children}</MessageText>
        )}
      </MessageBox>
    </Container>
  );
};

export default AssistenteMessage;
