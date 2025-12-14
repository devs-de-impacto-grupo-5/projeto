import { PiHeadsetFill, PiPlantFill, PiFileTextFill, PiHandshakeFill, PiBellFill } from 'react-icons/pi';
import { useNavigate } from 'react-router-dom';
import MenuCard from '../../components/MenuCard';
import { ReactComponent as ProdutorIcon } from '../../assets/svgs/produtor.svg';
import upperFormat from '../../assets/svgs/upperFormat.svg';
import downFormat from '../../assets/svgs/downFormat.svg';
import {
  Container,
  Header,
  HelpButton,
  UserSection,
  Avatar,
  UserInfo,
  Greeting,
  UserName,
  MenuTitle,
  MenuSubtitle,
  CardsGrid,
  TopRightBlob,
  BottomLeftBlob
} from './style';

const MenuProdutor = () => {
  const navigate = useNavigate();

  return (
    <Container>
      <TopRightBlob src={upperFormat} alt="" />
      <BottomLeftBlob src={downFormat} alt="" />
      
      <Header>
        <HelpButton onClick={() => console.log('Help')} aria-label="Ajuda">
          <PiHeadsetFill size={24} />
        </HelpButton>
      </Header>

      <UserSection>
        <Avatar onClick={() => navigate('/admin/dash')} style={{ cursor: 'pointer' }}>
          <ProdutorIcon width={32} height={32} />
        </Avatar>
        <UserInfo>
          <Greeting>Bom dia,</Greeting>
          <UserName>João Silva</UserName>
        </UserInfo>
      </UserSection>

      <MenuTitle>Menu Principal</MenuTitle>
      <MenuSubtitle>O que quer fazer?</MenuSubtitle>

      <CardsGrid>
        <MenuCard
          title="Minhas Safras"
          icon={PiPlantFill}
          iconColor="#AE84E6"
          onClick={() => console.log('Minhas Safras')}
        />
        <MenuCard
          title="Meus Editais"
          icon={PiFileTextFill}
          iconColor="#B2E3AB"
          onClick={() => console.log('Meus editais')}
        />
        <MenuCard
          title="Propostas"
          icon={PiHandshakeFill}
          iconColor="#F9D67A"
          onClick={() => console.log('Propostas')}
        />
        <MenuCard
          title="Notificações"
          icon={PiBellFill}
          iconColor="#FFB6C1"
          onClick={() => console.log('Notificações')}
        />
      </CardsGrid>
    </Container>
  );
};

export default MenuProdutor;
