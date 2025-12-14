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
  projetoDeVenda
} from '../../constants/documents';

const EnviarDocumentoChat = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { documentoNome } = location.state || { documentoNome: 'Documento' };
  const subtipoUsuario = localStorage.getItem('subtipo_usuario');
  const [showFileUpload, setShowFileUpload] = useState(false);

  // Função para obter os steps corretos baseado no documento e tipo de produtor
  const getSteps = (nomeDocumento, subtipo) => {
    const isPF = subtipo === 'fornecedor_individual';
    const isPFGroup = subtipo === 'grupo_informal';
    const isPJ = subtipo === 'grupo_formal';

    // Mapeamento de documentos para steps
    const stepsMap = {
      'Declaração de Aptidão': isPF ? stepByStepDeclaracaoAptidaoPF : isPFGroup ? stepByStepDeclaracaoAptidaoPFGroup : stepByStepDeclaracaoAptidaoPJ,
      'Regularidade Federal': isPF ? stepByStepRegularidadeFederalPF : isPFGroup ? stepByStepRegularidadeFederalPFGroup : stepByStepRegularidadeFederalPJ,
      'Regularidade Municipal': isPF ? stepByStepRegularidadeMunicipalPF : isPFGroup ? stepByStepRegularidadeMunicipalPFGroup : stepByStepRegularidadeMunicipalPJ,
      'Regularidade Trabalhista': isPF ? stepByStepRegularidadeTrabalhistaPF : isPFGroup ? stepByStepRegularidadeTrabalhistaPFGroup : stepByStepRegularidadeTrabalhistaPJ,
      'FGTS': stepByStepFGTS,
      'Estatuto/Ata': stepByStepEstatutoAta,
      'Controle de Limites': [], // TODO: Adicionar step-by-step
      'Projeto de Venda': projetoDeVenda
    };

    return stepsMap[nomeDocumento] || [];
  };

  // Gera mensagens iniciais: todos os steps em uma única mensagem
  const steps = getSteps(documentoNome, subtipoUsuario);
  const stepsText = steps.map((step, index) => `**${index + 1}.** ${step}`).join('\n\n');
  const initialMessages = [
    { type: 'assistente', text: stepsText },
    { type: 'assistente', text: 'Você conseguiu emitir o documento?' },
    {
      type: 'options',
      options: [
        { label: 'SIM', value: 'sim' },
        { label: 'NÃO', value: 'nao' }
      ]
    }
  ];

  const handleFileUpload = (file, setMessages) => {
    // Adiciona mensagem mostrando o nome do arquivo
    setMessages(prev => [...prev, {
      type: 'produtor',
      text: `📎 ${file.name}`
    }]);

    // TODO: Enviar arquivo para API
    console.log('Arquivo selecionado:', file);

    // Mensagem de sucesso
    setMessages(prev => [...prev, {
      type: 'assistente',
      text: 'Documento recebido com sucesso! Aguarde a análise.'
    }]);

    // Esconde upload e redireciona após 2 segundos
    setTimeout(() => {
      navigate('/documentos-produtor');
    }, 2000);
  };

  const handleOptionSelect = (value, setMessages) => {
    if (value === 'sim') {
      // Remove os botões
      setMessages(prev => prev.filter(msg => msg.type !== 'options'));

      // Adiciona resposta do usuário
      setMessages(prev => [...prev, { type: 'produtor', text: 'SIM' }]);

      // Pede para enviar o arquivo
      setMessages(prev => [...prev, {
        type: 'assistente',
        text: 'Ótimo! Por favor, envie o arquivo do documento.'
      }]);

      // Mostra input de arquivo
      setShowFileUpload(true);
    } else if (value === 'nao') {
      // Remove os botões
      setMessages(prev => prev.filter(msg => msg.type !== 'options'));

      // Adiciona resposta do usuário
      setMessages(prev => [...prev, { type: 'produtor', text: 'NÃO' }]);

      // Envia mensagem de ajuda
      setMessages(prev => [...prev, {
        type: 'assistente',
        text: 'Procure a prefeitura da sua cidade para obter ajuda.'
      }]);
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
