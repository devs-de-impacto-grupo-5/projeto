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
  const allChecked = documentos.length > 0 && documentos.every((doc) => doc.status === 'enviado');

  useEffect(() => {
    const subtipoUsuario = localStorage.getItem('subtipo_usuario');

    let docsLista = [];
    if (subtipoUsuario === 'fornecedor_individual') {
      docsLista = produtorIndividualDocs;
    } else if (subtipoUsuario === 'grupo_informal') {
      docsLista = grupoInformalDocs;
    } else if (subtipoUsuario === 'grupo_formal') {
      docsLista = grupoFormalDocs;
    }

    const enviados = JSON.parse(localStorage.getItem('docs_enviados') || '[]');
    const docsComStatus = docsLista.map((nomeDoc) => ({
      nome: nomeDoc,
      status: enviados.includes(nomeDoc) ? 'enviado' : 'pendente',
    }));

    setDocumentos(docsComStatus);
  }, []);

  const handleOpenUpload = (docNome) => {
    navigate('/enviar-documento', {
      state: {
        documentoNome: docNome,
      },
    });
  };

  return (
    <PageContainer>
      <Header onBack={() => console.log('Back')} onHelp={() => console.log('Help')} />
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
            onClick={() => handleOpenUpload(doc.nome)}
          />
        ))}
      </Container>
      <BottomAction
        buttonText="Avançar para Produção"
        description="Complete os envios para continuar"
        disabled={!allChecked}
        onClick={() => navigate('/menu-produtor')}
      />
    </PageContainer>
  );
};

export default Documentos;
