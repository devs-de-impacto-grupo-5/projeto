import React from 'react';
import { Container, IconWrapper, MessageBox, MessageText, TypingIndicator, Dot } from './style';
import { ReactComponent as Logo } from '../../assets/svgs/logo.svg';

const AssistenteMessage = ({ children }) => {
  const isTyping = children === 'typing';

  // Processa markdown simples: **texto** -> <strong>texto</strong>
  const processMarkdown = (text) => {
    if (typeof text !== 'string') return text;

    // Divide em linhas primeiro
    const lines = text.split('\n');

    return lines.map((line, lineIndex) => {
      const parts = line.split(/(\*\*.*?\*\*)/g);
      const processedLine = parts.map((part, partIndex) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          const boldText = part.slice(2, -2);
          return <strong key={`${lineIndex}-${partIndex}`}>{boldText}</strong>;
        }
        return part;
      });

      return (
        <React.Fragment key={lineIndex}>
          {processedLine}
          {lineIndex < lines.length - 1 && <br />}
        </React.Fragment>
      );
    });
  };

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
          <MessageText>{processMarkdown(children)}</MessageText>
        )}
      </MessageBox>
    </Container>
  );
};

export default AssistenteMessage;
