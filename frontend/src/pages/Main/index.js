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
  return (
    <Container>
      <TopShape src={upperFormat} alt="" />
      <BottomShape src={downFormat} alt="" />
      
      <Header>
        <UserInfo>
          <Avatar src={iconProfile} alt="João Silva" />
          <Greeting>
            <GreetingText>Bom dia,</GreetingText>
            <UserName>João Silva</UserName>
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

