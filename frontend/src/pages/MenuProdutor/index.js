import { PiHeadsetFill, PiPlantFill, PiFileTextFill, PiHandshakeFill, PiBellFill } from 'react-icons/pi';
import { useNavigate } from 'react-router-dom';
import MenuCard from '../../components/MenuCard';
import { ReactComponent as ProdutorIcon } from '../../assets/svgs/produtor.svg';
import {
  Container,
  Content,
  Header,
  HelpButton,
  UserSection,
  Avatar,
  UserInfo,
  Greeting,
  UserName,
  HeroCard,
  HeroTitle,
  HeroSubtitle,
  ActionsRow,
  PillAction,
  SectionTitle,
  MenuSubtitle,
  CardsGrid
} from './style';

const MenuProdutor = () => {
  const navigate = useNavigate();
  const nome = localStorage.getItem('user_name');

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return `Bom dia,`;
    if (hour < 18) return `Boa tarde,`;
    return `Boa noite,`;
  };

  return (
    <Container>
      <Content>
        <Header>
          <UserSection>
            <Avatar onClick={() => navigate('/admin/dash')} style={{ cursor: 'pointer' }}>
              <ProdutorIcon width={32} height={32} />
            </Avatar>
            <UserInfo>
              <Greeting>{getGreeting()}</Greeting>
              {nome && <UserName>{nome}</UserName>}
            </UserInfo>
          </UserSection>
          <HelpButton onClick={() => console.log('Help')} aria-label="Ajuda">
            <PiHeadsetFill size={22} />
          </HelpButton>
        </Header>

        <HeroCard>
          <div>
            <HeroTitle>Menu Principal</HeroTitle>
            <HeroSubtitle>Gerencie safras, editais e propostas em um só lugar.</HeroSubtitle>
            <ActionsRow>
              <PillAction onClick={() => navigate('/menu-produtor/editais')}>Meus editais</PillAction>
              <PillAction $ghost onClick={() => navigate('/menu-produtor/notificacoes')}>
                Notificações
              </PillAction>
            </ActionsRow>
          </div>
        </HeroCard>

        <SectionTitle>O que quer fazer?</SectionTitle>
        <MenuSubtitle>Escolha um atalho abaixo.</MenuSubtitle>

        <CardsGrid>
          <MenuCard
            title="Minhas Safras"
            icon={PiPlantFill}
            iconColor="#AE84E6"
            onClick={() => navigate('/menu-produtor/safras')}
          />
          <MenuCard
            title="Meus Editais"
            icon={PiFileTextFill}
            iconColor="#B2E3AB"
            onClick={() => navigate('/menu-produtor/editais')}
          />
          <MenuCard
            title="Propostas"
            icon={PiHandshakeFill}
            iconColor="#F9D67A"
            onClick={() => navigate('/menu-produtor/propostas')}
          />
          <MenuCard
            title="Notificações"
            icon={PiBellFill}
            iconColor="#FFB6C1"
            onClick={() => navigate('/menu-produtor/notificacoes')}
          />
        </CardsGrid>
      </Content>
    </Container>
  );
};

export default MenuProdutor;
