import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import EnviarDocumento from '../../components/EnviarDocumento';
import BottomAction from '../../components/BottomAction';
import { PageContainer, Container, Title, Description } from './style';
import { produtorIndividualDocs, grupoInformalDocs, grupoFormalDocs } from '../../constants/documents';

const Documentos = () => {
  const navigate = useNavigate();
  const [documentos, setDocumentos] = useState([]);

  useEffect(() => {
    // Busca subtipo do localStorage
    const subtipoUsuario = localStorage.getItem('subtipo_usuario');

    // Mapeia subtipo para a lista correta de documentos
    let docsLista = [];
    if (subtipoUsuario === 'fornecedor_individual') {
      docsLista = produtorIndividualDocs;
    } else if (subtipoUsuario === 'grupo_informal') {
      docsLista = grupoInformalDocs;
    } else if (subtipoUsuario === 'grupo_formal') {
      docsLista = grupoFormalDocs;
    }

    // Cria lista de documentos com status pendente por padrão
    const docsComStatus = docsLista.map(nomeDoc => ({
      nome: nomeDoc,
      status: 'pendente'
    }));

    setDocumentos(docsComStatus);
  }, []);

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
        {documentos.map((doc, index) => (
          <EnviarDocumento
            key={index}
            type={doc.status}
            title={doc.nome}
            subtitle={doc.status === 'pendente' ? 'Toque para enviar' : 'Recebido com sucesso'}
            onClick={() => navigate('/enviar-documento', { state: { documentoNome: doc.nome } })}
          />
        ))}
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
