import { Container, Title, IconWrapper } from './style';

const MenuCard = ({ title, icon: Icon, iconColor, onClick }) => {
  return (
    <Container onClick={onClick}>
      <Title>{title}</Title>
      {Icon && (
        <IconWrapper color={iconColor}>
          <Icon size={48} />
        </IconWrapper>
      )}
    </Container>
  );
};

export default MenuCard;
