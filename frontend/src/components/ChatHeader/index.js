import { FiArrowLeft } from 'react-icons/fi';
import { PiHeadsetFill } from 'react-icons/pi';
import { ReactComponent as Logo } from '../../assets/svgs/logo.svg';
import { Container, BackButton, LogoWrapper, TextContainer, Title, Subtitle, HelpButton } from './style';

const ChatHeader = ({ onBack, onHelp }) => {
  return (
    <Container>
      <BackButton onClick={onBack}>
        <FiArrowLeft size={24} />
      </BackButton>
      <LogoWrapper>
        <Logo width={32} height={32} />
      </LogoWrapper>
      <TextContainer>
        <Subtitle>Você está falando com...</Subtitle>
        <Title>Assistente Vitalis</Title>
      </TextContainer>
      <HelpButton onClick={onHelp}>
        <PiHeadsetFill size={24} />
      </HelpButton>
    </Container>
  );
};

export default ChatHeader;
