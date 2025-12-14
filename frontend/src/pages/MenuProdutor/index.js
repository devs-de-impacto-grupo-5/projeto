import { PiHeadsetFill } from 'react-icons/pi';
import { PiPlantFill } from 'react-icons/pi';
import MenuCard from '../../components/MenuCard';
import { ReactComponent as ProdutorIcon } from '../../assets/svgs/produtor.svg';
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
  CardsGrid
} from './style';

const MenuProdutor = () => {
  return (
    <Container>
      <Header>
        <HelpButton onClick={() => console.log('Help')}>
          <PiHeadsetFill size={24} />
        </HelpButton>
      </Header>

      <UserSection>
        <Avatar>
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
          title="Meus editais"
          onClick={() => console.log('Meus editais')}
        />
        <MenuCard
          title="Meus editais"
          onClick={() => console.log('Meus editais')}
        />
        <MenuCard
          title="Meus editais"
          onClick={() => console.log('Meus editais')}
        />
      </CardsGrid>
    </Container>
  );
};

export default MenuProdutor;
