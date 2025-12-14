import { FiArrowLeft } from 'react-icons/fi';
import { PiHeadsetFill } from 'react-icons/pi';
import { ReactComponent as Logo } from '../../assets/svgs/horizontal_logo.svg';
import { Container, BackButton, LogoWrapper, HelpButton } from './style';

const Header = ({ onBack, onHelp }) => {
  return (
    <Container>
      <BackButton onClick={onBack}>
        <FiArrowLeft size={24} />
      </BackButton>
      <LogoWrapper>
        <Logo height={40} />
      </LogoWrapper>
      <HelpButton onClick={onHelp}>
        <PiHeadsetFill size={24} />
      </HelpButton>
    </Container>
  );
};

export default Header;
