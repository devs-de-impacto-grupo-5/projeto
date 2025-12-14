import { FiCheck, FiChevronRight } from 'react-icons/fi';
import { MdOutlineDescription } from 'react-icons/md';
import { Container, IconWrapper, TextContainer, Title, Subtitle, ActionIcon } from './style';

const EnviarDocumento = ({ type = 'enviado', title, subtitle, onClick }) => {
  const isEnviado = type === 'enviado';

  return (
    <Container onClick={onClick} type={type}>
      <IconWrapper type={type}>
        {isEnviado ? (
          <FiCheck size={24} color="white" />
        ) : (
          <MdOutlineDescription size={24} color="white" />
        )}
      </IconWrapper>
      <TextContainer>
        <Title>{title}</Title>
        <Subtitle>{subtitle}</Subtitle>
      </TextContainer>
      {!isEnviado && (
        <ActionIcon>
          <FiChevronRight size={24} />
        </ActionIcon>
      )}
    </Container>
  );
};

export default EnviarDocumento;
