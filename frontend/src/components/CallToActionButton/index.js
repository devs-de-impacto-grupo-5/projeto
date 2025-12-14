import React from 'react';
import { Container, IconWrapper, Title, Subtitle, TextContainer, IconContainer } from './style';

const CallToActionButton = ({
  icon: Icon,
  iconBackgroundColor,
  iconColor,
  title,
  subtitle,
  to
}) => {
  return (
    <Container to={to}>
      <IconContainer>
        <IconWrapper backgroundColor={iconBackgroundColor}>
            <Icon color={iconColor} size={24} />
        </IconWrapper>
      </IconContainer>
      <TextContainer>
        <Title>{title}</Title>
        <Subtitle>{subtitle}</Subtitle>
      </TextContainer>
    </Container>
  );
};

export default CallToActionButton;
