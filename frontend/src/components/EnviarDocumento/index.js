import { FiCheck, FiChevronRight } from 'react-icons/fi';
import { MdOutlineDescription } from 'react-icons/md';
import { Container, IconWrapper, TextContainer, Title, Subtitle, ActionIcon } from './style';

const EnviarDocumento = ({ type = 'enviado', title, subtitle, onClick }) => {
  const isEnviado = type === 'enviado';

  return (
    <Container onClick={onClick} type={isEnviado ? 'enviado' : 'pendente'}>
      <IconWrapper type={isEnviado ? 'enviado' : 'pendente'}>
        {isEnviado ? <FiCheck size={24} color="white" /> : <MdOutlineDescription size={24} color="white" />}
      </IconWrapper>
      <TextContainer>
        <Title>{title}</Title>
        <Subtitle type={isEnviado ? 'enviado' : 'pendente'}>{subtitle}</Subtitle>
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
