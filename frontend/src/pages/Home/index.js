import React from 'react';
import { Container, ProdutorWrapper, ProdutorImage, LogoWrapper, LogoImage, Slogan, Question, ButtonsWrapper, ChangeAccountType } from './style';
import produtorSvg from '../../assets/svgs/produtor.svg';
import logoSvg from '../../assets/svgs/horizontal_logo.svg';
import CallToActionButton from '../../components/CallToActionButton';
import { FiLogIn, FiHelpCircle } from 'react-icons/fi';

const Home = () => {
  return (
    <Container>
      <LogoWrapper>
        <LogoImage src={logoSvg} alt="Logo" />
      </LogoWrapper>
      <Slogan>Vital para quem produz, essencial para quem aprende</Slogan>
      <ProdutorWrapper>
        <ProdutorImage src={produtorSvg} alt="Produtor" />
      </ProdutorWrapper>
      <Question>Como você quer começar?</Question>
      <ButtonsWrapper>
        <CallToActionButton
          icon={FiLogIn}
          iconBackgroundColor="#E8D5F2"
          iconColor="#6B2E9E"
          title="Entrar no Vitalis"
          subtitle="Comece a usar o Vitalis"
          to="/login"
        />
        <CallToActionButton
          icon={FiHelpCircle}
          iconBackgroundColor="#FFF4E0"
          iconColor="#F5A623"
          title="Precisa de ajuda?"
          subtitle="Entenda como usar"
          to="/help"
        />
      </ButtonsWrapper>
      <ChangeAccountType onClick={() => { window.location.href = '/admin/login'; }}>
        Sou entidade
      </ChangeAccountType>
    </Container>
  );
};

export default Home;
