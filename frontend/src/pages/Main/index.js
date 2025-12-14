import React from 'react';
import { 
  Container, 
  TopShape, 
  BottomShape, 
  Header, 
  UserInfo, 
  Avatar, 
  Greeting, 
  GreetingText, 
  UserName, 
  SupportButton, 
  Content, 
  Title, 
  Subtitle, 
  Grid, 
  Card, 
  CardTitle, 
  SvgCard,
  SvgImage,
  SvgCardTitle
} from './style';
import { FiHeadphones } from 'react-icons/fi';
import upperFormat from '../../assets/svgs/upperFormat.svg';
import downFormat from '../../assets/svgs/downFormat.svg';
import iconProfile from '../../assets/png/iconProfile.png';
import buttonNote from '../../assets/svgs/buttonNote.svg';
import buttonFlower from '../../assets/svgs/buttonFlower.svg';
import whiteRect from '../../assets/svgs/whiteRect.svg';

const Main = () => {
  const nome = localStorage.getItem('user_name');

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Bom dia,';
    if (hour < 18) return 'Boa tarde,';
    return 'Boa noite,';
  };

  return (
    <Container>
      <TopShape src={upperFormat} alt="" />
      <BottomShape src={downFormat} alt="" />
      
      <Header>
        <UserInfo>
          <Avatar src={iconProfile} alt={nome || 'Usuário'} />
          <Greeting>
            <GreetingText>{getGreeting()}</GreetingText>
            {nome && <UserName>{nome}</UserName>}
          </Greeting>
        </UserInfo>
        <SupportButton>
          <FiHeadphones />
        </SupportButton>
      </Header>

      <Content>
        <Title>Menu Principal</Title>
        <Subtitle>O que quer fazer?</Subtitle>

        <Grid>
          <SvgCard>
            <SvgImage src={buttonFlower} alt="" />
            <SvgCardTitle>Minhas Safras</SvgCardTitle>
          </SvgCard>

          <SvgCard>
            <SvgImage src={whiteRect} alt="" />
            <SvgCardTitle>Meus editais</SvgCardTitle>
          </SvgCard>

          <SvgCard>
            <SvgImage src={whiteRect} alt="" />
            <SvgCardTitle>Meus editais</SvgCardTitle>
          </SvgCard>

          <SvgCard>
            <SvgImage src={buttonNote} alt="" />
            <SvgCardTitle>Meus editais</SvgCardTitle>
          </SvgCard>
        </Grid>
      </Content>
    </Container>
  );
};

export default Main;

