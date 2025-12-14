import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Chat from '../../components/Chat';
import {
  stepByStepDeclaracaoAptidaoPF,
  stepByStepDeclaracaoAptidaoPFGroup,
  stepByStepDeclaracaoAptidaoPJ,
  stepByStepRegularidadeFederalPF,
  stepByStepRegularidadeFederalPFGroup,
  stepByStepRegularidadeFederalPJ,
  stepByStepRegularidadeMunicipalPF,
  stepByStepRegularidadeMunicipalPFGroup,
  stepByStepRegularidadeMunicipalPJ,
  stepByStepRegularidadeTrabalhistaPF,
  stepByStepRegularidadeTrabalhistaPFGroup,
  stepByStepRegularidadeTrabalhistaPJ,
  stepByStepEstatutoAta,
  stepByStepFGTS,
} from '../../constants/documents';

const EnviarDocumentoChat = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { documentoNome } = location.state || { documentoNome: 'Documento' };
  const subtipoUsuario = localStorage.getItem('subtipo_usuario');
  const [showFileUpload, setShowFileUpload] = useState(false);

  const getProjetoDeVendaJourney = (subtipo) => {
    if (subtipo === 'grupo_formal') {
      return `Com base no documento enviado, listei abaixo **todos** os campos que constam no modelo de projeto para **Grupos Formais (Cooperativas/Associações)**:

**Cabeçalho**
- Identificação da proposta de atendimento ao Edital/Chamada Pública Nº

**I – Identificação dos Fornecedores (Grupo Formal)**
- Nome do Proponente
- CNPJ
- Endereço
- Município/UF
- E-mail
- DDD/Fone
- CEP
- Nº DAP Jurídica
- Banco
- Agência / Conta Corrente
- Nº de Associados
- Nº de Associados de acordo com a Lei nº 11.326/2006
- Nº de Associados com DAP Física
- Nome do representante legal
- CPF (do representante)
- DDD/Fone (do representante)
- Endereço (do representante)
- Município/UF (do representante)

**II – Identificação da Entidade Executora do PNAE/FNDE/MEC**
- Nome da Entidade
- CNPJ
- Município/UF
- Endereço
- DDD/Fone
- Nome do representante e e-mail
- CPF (do representante da entidade)

**III – Relação de Produtos**
- Produto
- Unidade
- Quantidade
- Preço de Aquisição Unitário
- Preço de Aquisição Total
- Cronograma de Entrega dos produtos

**Assinaturas**
- Local e Data
- Assinatura do Representante do Grupo Formal
- Fone/E-mail

Gostaria que eu organizasse esses campos em uma tabela ou formato de checklist para facilitar o preenchimento?`;
    }

    if (subtipo === 'grupo_informal') {
      return `Com base no documento enviado, listei abaixo **todos** os campos que constam no modelo de projeto para **Grupos Informais**:

**Cabeçalho**
- Identificação da proposta de atendimento ao Edital/Chamada Pública Nº

**I – Identificação dos Fornecedores (Grupo Informal)**
- Nome do Proponente
- CPF
- Endereço
- Município/UF
- CEP
- E-mail (quando houver)
- Fone
- Organizado por Entidade Articuladora (Sim/Não)
- Nome da Entidade Articuladora (quando houver)
- E-mail/Fone (da entidade articuladora)

**II – Fornecedores Participantes**
- Nome do Agricultor(a) Familiar
- CPF
- DAP
- Banco
- Nº Agência
- Nº Conta Corrente

**III – Identificação da Entidade Executora do PNAE/FNDE/MEC**
- Nome da Entidade
- CNPJ
- Município
- Endereço
- DDD/Fone
- Nome do representante e e-mail
- CPF (do representante)

**III – Relação de Fornecedores e Produtos**
- Identificação do Agricultor(a) Familiar
- Produto
- Unidade
- Quantidade
- Preço de Aquisição/Unidade
- Valor Total

**IV – Totalização por Produto**
- Produto
- Unidade
- Quantidade
- Preço/Unidade
- Valor Total por Produto
- Cronograma de Entrega dos Produtos
- Total do projeto

**Assinaturas**
- Local e Data
- Assinatura do Representante do Grupo Informal
- Fone/E-mail e CPF (do representante)
- Assinatura dos Agricultores(as) Fornecedores(as)

Gostaria que eu organizasse esses campos em uma tabela ou formato de checklist para facilitar o preenchimento?`;
    }

    return `Com base no documento enviado, listei abaixo **todos** os campos que constam no modelo de projeto para **Fornecedores Individuais**:

**Cabeçalho**
- Identificação da proposta de atendimento ao Edital/Chamada Pública Nº

**I – Identificação do Fornecedor (Individual)**
- Nome do Proponente
- CPF
- Endereço
- Município/UF
- CEP
- Nº da DAP Física
- DDD/Fone
- E-mail (quando houver)
- Banco
- Nº da Agência
- Nº da Conta Corrente

**II – Relação dos Produtos**
- Produto
- Unidade
- Quantidade
- Preço de Aquisição Unitário
- Preço de Aquisição Total
- Cronograma de Entrega dos produtos

**III – Identificação da Entidade Executora do PNAE/FNDE/MEC**
- Nome (da entidade)
- CNPJ
- Município
- Endereço
- Fone
- Nome do Representante Legal
- CPF (do representante)

**Assinaturas**
- Local e Data
- Assinatura do Fornecedor Individual
- CPF

Gostaria que eu organizasse esses campos em uma tabela ou formato de checklist para facilitar o preenchimento?`;
  };

  const getSteps = (nomeDocumento, subtipo) => {
    const isPF = subtipo === 'fornecedor_individual';
    const isPFGroup = subtipo === 'grupo_informal';
    const isPJ = subtipo === 'grupo_formal';

    if (nomeDocumento === 'Projeto de Venda') {
      return getProjetoDeVendaJourney(subtipo);
    }

    const stepsMap = {
      'Declaração de Aptidão': isPF
        ? stepByStepDeclaracaoAptidaoPF
        : isPFGroup
          ? stepByStepDeclaracaoAptidaoPFGroup
          : stepByStepDeclaracaoAptidaoPJ,
      'Regularidade Federal': isPF
        ? stepByStepRegularidadeFederalPF
        : isPFGroup
          ? stepByStepRegularidadeFederalPFGroup
          : stepByStepRegularidadeFederalPJ,
      'Regularidade Municipal': isPF
        ? stepByStepRegularidadeMunicipalPF
        : isPFGroup
          ? stepByStepRegularidadeMunicipalPFGroup
          : stepByStepRegularidadeMunicipalPJ,
      'Regularidade Trabalhista': isPF
        ? stepByStepRegularidadeTrabalhistaPF
        : isPFGroup
          ? stepByStepRegularidadeTrabalhistaPFGroup
          : isPJ
            ? stepByStepRegularidadeTrabalhistaPJ
            : [],
      FGTS: stepByStepFGTS,
      'Estatuto/Ata': stepByStepEstatutoAta,
      'Controle de Limites': [],
    };

    return stepsMap[nomeDocumento] || [];
  };

  const steps = getSteps(documentoNome, subtipoUsuario);
  const stepsText = Array.isArray(steps)
    ? steps.map((step, index) => `**${index + 1}.** ${step}`).join('\n\n')
    : steps;
  const initialMessages = [
    { type: 'assistente', text: stepsText },
    { type: 'assistente', text: 'Você conseguiu emitir o documento?' },
    {
      type: 'options',
      options: [
        { label: 'SIM', value: 'sim' },
        { label: 'NÃO', value: 'nao' },
      ],
    },
  ];

  const handleFileUpload = (file, setMessages) => {
    setMessages((prev) => [...prev, { type: 'produtor', text: `Arquivo enviado: ${file.name}` }]);

    // TODO: Enviar arquivo para API real
    console.log('Arquivo selecionado:', file);

    setMessages((prev) => [
      ...prev,
      {
        type: 'assistente',
        text: 'Documento recebido com sucesso! Aguarde a análise.',
      },
    ]);

    // Marca documento como enviado localmente
    const enviados = new Set(JSON.parse(localStorage.getItem('docs_enviados') || '[]'));
    enviados.add(documentoNome);
    localStorage.setItem('docs_enviados', JSON.stringify(Array.from(enviados)));

    setTimeout(() => {
      navigate('/documentos-produtor');
    }, 1500);
  };

  const handleOptionSelect = (value, setMessages) => {
    if (value === 'sim') {
      setMessages((prev) => prev.filter((msg) => msg.type !== 'options'));
      setMessages((prev) => [...prev, { type: 'produtor', text: 'SIM' }]);
      setMessages((prev) => [
        ...prev,
        { type: 'assistente', text: 'Ótimo! Por favor, envie o arquivo do documento.' },
      ]);
      setShowFileUpload(true);
    } else if (value === 'nao') {
      setMessages((prev) => prev.filter((msg) => msg.type !== 'options'));
      setMessages((prev) => [...prev, { type: 'produtor', text: 'NÃO' }]);
      setMessages((prev) => [
        ...prev,
        { type: 'assistente', text: 'Procure a prefeitura da sua cidade para obter ajuda.' },
      ]);
    }
  };

  return (
    <Chat
      onBack={() => navigate('/documentos-produtor')}
      onHelp={() => console.log('Help')}
      initialMessages={initialMessages}
      onOptionSelect={handleOptionSelect}
      showInput={false}
      showFileUpload={showFileUpload}
      onFileUpload={handleFileUpload}
    />
  );
};

export default EnviarDocumentoChat;
