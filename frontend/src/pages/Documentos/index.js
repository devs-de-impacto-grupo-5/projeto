import Header from '../../components/Header';
import EnviarDocumento from '../../components/EnviarDocumento';
import BottomAction from '../../components/BottomAction';
import { PageContainer, Container, Title, Description } from './style';

const Documentos = () => {
  return (
    <PageContainer>
      <Header
        onBack={() => console.log('Back')}
        onHelp={() => console.log('Help')}
      />
      <Container>
        <Title>Verificação de documentos</Title>
        <Description>
          Para que você apareça nas oportunidades, precisamos confirmar alguns dados. É rapidinho!
        </Description>
        <EnviarDocumento
          type="enviado"
          title="Documento"
          subtitle="Recebido com sucesso"
        />
        <EnviarDocumento
          type="pendente"
          title="Documento"
          subtitle="Toque para enviar"
          onClick={() => console.log('Enviar documento')}
        />
        <EnviarDocumento
          type="pendente"
          title="Documento"
          subtitle="Toque para enviar"
          onClick={() => console.log('Enviar documento')}
        />
        <EnviarDocumento
          type="pendente"
          title="Documento"
          subtitle="Toque para enviar"
          onClick={() => console.log('Enviar documento')}
        />
        <EnviarDocumento
          type="pendente"
          title="Documento"
          subtitle="Toque para enviar"
          onClick={() => console.log('Enviar documento')}
        />
        <EnviarDocumento
          type="pendente"
          title="Documento"
          subtitle="Toque para enviar"
          onClick={() => console.log('Enviar documento')}
        />
      </Container>
      <BottomAction
        buttonText="Avançar para Produção"
        description="Complete os envios para continuar"
        onClick={() => console.log('Avançar')}
      />
    </PageContainer>
  );
};

export default Documentos;
