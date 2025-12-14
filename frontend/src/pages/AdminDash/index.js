import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Container,
  Header,
  HeaderContent,
  LogoImage,
  NavMenu,
  NavItem,
  UserProfile,
  UserName,
  UserRole,
  UserAvatar,
  MainContent,
  TopBar,
  SectionBadge,
  SectionMeta,
  PageHeader,
  PageTitle,
  PageSubtitle,
  ActionSection,
  CreateButton,
  GhostButton,
  ModalOverlay,
  ModalCard,
  ModalHeader,
  ModalTitle,
  CloseButton,
  ModalBody,
  DropZone,
  DropLabel,
  FileName,
  HelperText,
  ModalFooter,
  SubmitButton,
  SecondaryButton,
  InlineBadge,
  ProgressTrack,
  ProgressBar,
  ResultPanel,
  ResultTitle,
  ResultRow,
  ResultLabel,
  ResultValue,
  MatchList,
  MatchItem,
  MatchName,
  MatchMeta,
  Stepper,
  StepItem,
  StepDot,
  FooterActions,
  InfoList,
  InfoItem,
  StatsGrid,
  StatCard,
  StatIconWrapper,
  StatInfo,
  StatTitle,
  StatValue,
  FiltersBar,
  FiltersRow,
  SearchInputWrapper,
  SearchInput,
  FilterSelect,
  TableCard,
  TableContainer,
  TableHeader,
  TableRow,
  IdBadge,
  EditalInfo,
  EditalTitle,
  EditalMeta,
  DateText,
  StatusBadge,
  ActionButton,
  EmptyState,
  EmptyTitle,
  EmptyText,
  EmptyAction,
  PaginationWrapper,
  PageButton,
  ResultsText,
} from './style';

import logoSvg from '../../assets/svgs/horizontal_logo.svg';
import personImage from '../../assets/png/assetPerson.png';
import {
  FiSearch,
  FiPlus,
  FiChevronLeft,
  FiChevronRight,
  FiEye,
  FiFileText,
  FiCheckCircle,
  FiUsers,
} from 'react-icons/fi';
import { BsArrowRightShort } from 'react-icons/bs';

const AdminDash = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    total_demandas: 0,
    demandas_ativas: 0,
    total_candidatos: 0,
  });
  const [editais, setEditais] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('todos');
  const [dateOrder, setDateOrder] = useState('recentes');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const [uploadResult, setUploadResult] = useState(null);
  const [matchLoading, setMatchLoading] = useState(false);
  const [matchResult, setMatchResult] = useState(null);
  const [modalStep, setModalStep] = useState('input'); // input | summary | match
  const [userName, setUserName] = useState('Usuário');

  useEffect(() => {
    const storedName = localStorage.getItem('user_name');
    if (storedName) {
      setUserName(storedName);
    }

    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        const headers = {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        };

        const statsResponse = await fetch('https://rj-devs-impacto-api.onrender.com/admin/relatorio', { headers });
        if (statsResponse.ok) {
          const statsData = await statsResponse.json();
          setStats({
            total_demandas: statsData.total_demandas,
            demandas_ativas: statsData.demandas_publicadas_ultimos_30_dias,
            total_candidatos: statsData.total_propostas,
          });
        }

        const editaisResponse = await fetch('https://rj-devs-impacto-api.onrender.com/admin/dashboard/editais', { headers });
        if (editaisResponse.ok) {
          const editaisData = await editaisResponse.json();
          setEditais(editaisData);
        }
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const formatDate = (dateString) => {
    const options = { day: 'numeric', month: 'short', year: 'numeric' };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
  };

  const statusLabel = (status) => {
    switch (status) {
      case 'draft':
        return 'Rascunho';
      case 'published':
      case 'ativo':
        return 'Ativo';
      case 'encerrado':
        return 'Encerrado';
      default:
        return status || 'Desconhecido';
    }
  };

  const filteredEditais = useMemo(() => {
    let lista = [...editais];

    if (statusFilter !== 'todos') {
      lista = lista.filter((item) => {
        const key = item.status === 'published' ? 'ativo' : item.status;
        return key === statusFilter;
      });
    }

    if (searchTerm.trim()) {
      const termo = searchTerm.trim().toLowerCase();
      lista = lista.filter(
        (item) =>
          String(item.id).padStart(2, '0').includes(termo) ||
          (item.titulo && item.titulo.toLowerCase().includes(termo)),
      );
    }

    lista.sort((a, b) => {
      const dataA = new Date(a.data).getTime();
      const dataB = new Date(b.data).getTime();
      return dateOrder === 'recentes' ? dataB - dataA : dataA - dataB;
    });

    return lista;
  }, [editais, searchTerm, statusFilter, dateOrder]);

  const resetModalState = useCallback(() => {
    setFile(null);
    setUploading(false);
    setUploadError('');
    setUploadResult(null);
    setMatchResult(null);
    setMatchLoading(false);
    setModalStep('input');
  }, []);

  const openModal = () => {
    resetModalState();
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  const handleFileChange = (event) => {
    const selected = event.target.files?.[0];
    if (selected) {
      setFile(selected);
      setUploadError('');
    }
  };

  const uploadPdf = async () => {
    if (!file) {
      setUploadError('Selecione um arquivo PDF para continuar.');
      return;
    }

    setUploading(true);
    setUploadError('');
    setUploadResult(null);
    setMatchResult(null);

    const formData = new FormData();
    formData.append('arquivo', file);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('https://rj-devs-impacto-api.onrender.com/editais/processar', {
        method: 'POST',
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
        body: formData,
      });

      const data = await response.json();
      if (!response.ok || data.success === false) {
        throw new Error(data.erro || 'Erro ao processar o edital');
      }

      setUploadResult(data);
      setModalStep('summary');
    } catch (error) {
      console.error(error);
      setUploadError(error.message || 'Não foi possível processar o edital.');
    } finally {
      setUploading(false);
    }
  };

  const goToMatchStep = () => {
    setModalStep('match');
    if (uploadResult && !matchResult && !matchLoading) {
      triggerMatch(uploadResult);
    }
  };

  const saveReport = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('https://rj-devs-impacto-api.onrender.com/admin/relatorio/download', {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      });

      if (!response.ok) {
        throw new Error('Não foi possível salvar o relatório.');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'relatorio_editais.csv';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      setUploadError(error.message || 'Falha ao salvar relatório.');
    }
  };

  const triggerMatch = async (data) => {
    const versaoId = Number(data?.rascunho_db_id || data?.rascunho_id || data?.versao_demanda_id);
    if (!versaoId || Number.isNaN(versaoId)) {
      setMatchResult({
        status: 'pending',
        message: 'Rascunho criado. O match precisa de uma versão de demanda publicada para rodar.',
      });
      return;
    }

    setMatchLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`https://rj-devs-impacto-api.onrender.com/match/execute/${versaoId}?trigger=manual_api`, {
        method: 'POST',
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      });
      const matchData = await response.json();
      if (!response.ok) {
        throw new Error(matchData.detail || 'Não foi possível buscar produtores próximos.');
      }
      setMatchResult(matchData);
    } catch (error) {
      console.error(error);
      setMatchResult({ status: 'error', message: error.message || 'Erro ao buscar produtores próximos.' });
    } finally {
      setMatchLoading(false);
    }
  };

  const handleExportReport = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('https://rj-devs-impacto-api.onrender.com/admin/relatorio/download', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'relatorio_editais.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        console.error('Erro ao baixar relatório');
      }
    } catch (error) {
      console.error('Erro na requisição:', error);
    }
  };

  return (
    <Container>
      <Header>
        <HeaderContent>
          <Link to="/admin/dash">
            <LogoImage src={logoSvg} alt="Vitalis" />
          </Link>

          <NavMenu aria-label="Navegação principal">
            <NavItem to="/admin/dash" $active>Início</NavItem>
            <NavItem to="/admin/info">Relatórios</NavItem>
            <NavItem to="/admin/prod">
              Produtores
            </NavItem>
          </NavMenu>

          <UserProfile to="/admin/profile">
            <div>
              <UserName>{userName}</UserName>
              <UserRole>Admin</UserRole>
            </div>
            <UserAvatar src={personImage} alt="Admin" />
          </UserProfile>
        </HeaderContent>
      </Header>

      <MainContent>
        <TopBar>
          <SectionBadge>Admin • Painel</SectionBadge>
          <SectionMeta>Atualizado em tempo real com os dados dos editais</SectionMeta>
        </TopBar>

        <ActionSection>
          <PageHeader>
            <PageTitle>Gestão de Editais</PageTitle>
            <PageSubtitle>
              Organize, publique e acompanhe o desempenho dos editais em um só lugar.
            </PageSubtitle>
          </PageHeader>

          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <GhostButton type="button" onClick={handleExportReport}>
              <BsArrowRightShort size={18} />
              Exportar relatório
            </GhostButton>
            <CreateButton type="button" onClick={openModal}>
              <FiPlus size={18} />
              Novo edital
            </CreateButton>
          </div>
        </ActionSection>

        <StatsGrid>
          <StatCard $borderColor="#6B2E9E">
            <StatIconWrapper>
              <FiFileText size={22} />
            </StatIconWrapper>
            <StatInfo>
              <StatTitle>Total de Editais</StatTitle>
              <StatValue>{loading ? '...' : stats.total_demandas}</StatValue>
            </StatInfo>
          </StatCard>

          <StatCard $borderColor="#27AE60">
            <StatIconWrapper>
              <FiCheckCircle size={22} />
            </StatIconWrapper>
            <StatInfo>
              <StatTitle>Editais Ativos</StatTitle>
              <StatValue>{loading ? '...' : stats.demandas_ativas}</StatValue>
            </StatInfo>
          </StatCard>

          <StatCard $borderColor="#2D9CDB">
            <StatIconWrapper>
              <FiUsers size={22} />
            </StatIconWrapper>
            <StatInfo>
              <StatTitle>Candidatos</StatTitle>
              <StatValue>{loading ? '...' : stats.total_candidatos}</StatValue>
            </StatInfo>
          </StatCard>
        </StatsGrid>

        <FiltersBar>
          <SearchInputWrapper>
            <FiSearch size={20} color="#A0A0A0" />
            <SearchInput
              placeholder="Buscar por ID ou título"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              aria-label="Buscar edital"
            />
          </SearchInputWrapper>

          <FiltersRow>
            <FilterSelect
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              aria-label="Filtrar status"
            >
              <option value="todos">Todos os status</option>
              <option value="ativo">Ativo</option>
              <option value="draft">Rascunho</option>
              <option value="encerrado">Encerrado</option>
            </FilterSelect>

            <FilterSelect
              value={dateOrder}
              onChange={(e) => setDateOrder(e.target.value)}
              aria-label="Ordenar por data"
            >
              <option value="recentes">Mais recentes</option>
              <option value="antigos">Mais antigos</option>
            </FilterSelect>
          </FiltersRow>
        </FiltersBar>

        <TableCard>
          <TableContainer>
            <TableHeader>
              <div>ID</div>
              <div>Edital</div>
              <div>Candidatos</div>
              <div>Data</div>
              <div>Status</div>
              <div>Ações</div>
            </TableHeader>

            {loading ? (
              <div style={{ padding: '24px', textAlign: 'center', fontWeight: 700, color: '#4B5563' }}>
                Carregando dados...
              </div>
            ) : filteredEditais.length === 0 ? (
              <EmptyState>
                <EmptyTitle>Nenhum edital encontrado</EmptyTitle>
                <EmptyText>
                  Ajuste os filtros ou crie um novo edital para começar a acompanhar os resultados.
                </EmptyText>
                <EmptyAction type="button">
                  <FiPlus size={16} />
                  Criar edital
                </EmptyAction>
              </EmptyState>
            ) : (
              filteredEditais.map((edital) => (
                <TableRow key={edital.id}>
                  <IdBadge>{String(edital.id).padStart(2, '0')}</IdBadge>

                  <EditalInfo>
                    <EditalTitle>{edital.titulo}</EditalTitle>
                    <EditalMeta>ID: {edital.id}</EditalMeta>
                  </EditalInfo>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <FiUsers size={16} color="#4B5563" />
                    <span style={{ fontWeight: 600, color: '#111827' }}>{edital.candidatos}</span>
                  </div>

                  <DateText>{formatDate(edital.data)}</DateText>

                  <StatusBadge $status={edital.status}>{statusLabel(edital.status)}</StatusBadge>

                  <ActionButton
                    type="button"
                    aria-label={`Visualizar edital ${edital.titulo}`}
                    onClick={() => navigate(`/admin/edit/${edital.id}`)}
                  >
                    <FiEye size={18} />
                    Detalhes
                  </ActionButton>
                </TableRow>
              ))
            )}
          </TableContainer>

          <PaginationWrapper>
            <ResultsText>Mostrando {filteredEditais.length} resultados</ResultsText>
            <div style={{ display: 'flex', gap: '8px' }}>
              <PageButton disabled>
                <FiChevronLeft size={20} />
              </PageButton>
              <PageButton $active>1</PageButton>
              <PageButton>2</PageButton>
              <PageButton>3</PageButton>
              <PageButton>
                <FiChevronRight size={20} />
              </PageButton>
            </div>
          </PaginationWrapper>
        </TableCard>

        {isModalOpen && (
          <ModalOverlay>
            <ModalCard role="dialog" aria-modal="true">
              <ModalHeader>
                <ModalTitle>Publicar novo edital</ModalTitle>
                <CloseButton onClick={closeModal} aria-label="Fechar modal">
                  ×
                </CloseButton>
              </ModalHeader>

              <ModalBody>
                <Stepper>
                  <StepItem $active={modalStep !== 'match'}>
                    <StepDot $active={modalStep !== 'match'} />
                    Resumo do edital (Gemini)
                  </StepItem>
                  <StepItem $active={modalStep === 'match'}>
                    <StepDot $active={modalStep === 'match'} />
                    Produtores recomendados
                  </StepItem>
                </Stepper>

                <DropZone>
                  <DropLabel>
                    <strong>Envie o PDF do edital</strong>
                    <HelperText>O Gemini extrai os itens para gerar um rascunho automático.</HelperText>
                  </DropLabel>
                  <input
                    type="file"
                    accept="application/pdf"
                    onChange={handleFileChange}
                    aria-label="Selecionar arquivo PDF"
                  />
                  {file && <FileName>{file.name}</FileName>}
                  {uploadError && <HelperText style={{ color: '#EF4444' }}>{uploadError}</HelperText>}
                  {uploading && (
                    <div>
                      <HelperText>Processando edital...</HelperText>
                      <ProgressTrack>
                        <ProgressBar style={{ width: '75%' }} />
                      </ProgressTrack>
                    </div>
                  )}
                </DropZone>

                {uploadResult && modalStep !== 'match' && (
                  <ResultPanel>
                    <ResultTitle>Rascunho gerado</ResultTitle>
                    <ResultRow>
                      <ResultLabel>Título</ResultLabel>
                      <ResultValue>{uploadResult.preview?.titulo || 'Sem título'}</ResultValue>
                    </ResultRow>
                    <ResultRow>
                      <ResultLabel>Resumo</ResultLabel>
                      <ResultValue>{uploadResult.preview?.resumo || '---'}</ResultValue>
                    </ResultRow>
                    <ResultRow>
                      <ResultLabel>Itens encontrados</ResultLabel>
                      <InlineBadge>{uploadResult.num_itens} itens</InlineBadge>
                    </ResultRow>
                  </ResultPanel>
                )}

                {matchLoading && (
                  <ResultPanel>
                    <ResultTitle>Buscando produtores próximos...</ResultTitle>
                    <HelperText>Executando match automático baseado no edital processado.</HelperText>
                  </ResultPanel>
                )}

                {modalStep === 'match' && matchResult && matchResult.opcoes && (
                  <ResultPanel>
                    <ResultTitle>Produtores próximos</ResultTitle>
                    <MatchList>
                      {matchResult.opcoes.map((opt, index) => (
                        <MatchItem key={index}>
                          <MatchName>
                            {opt.tipo === 'individual' ? 'Produtor' : 'Grupo'} • {opt.score_agregado}%
                          </MatchName>
                          <MatchMeta>{opt.produtores.map((p) => p.nome).join(', ')}</MatchMeta>
                        </MatchItem>
                      ))}
                    </MatchList>
                  </ResultPanel>
                )}

                {modalStep === 'match' && matchResult && matchResult.status === 'pending' && (
                  <ResultPanel>
                    <ResultTitle>Match pendente</ResultTitle>
                    <HelperText>{matchResult.message}</HelperText>
                  </ResultPanel>
                )}

                {modalStep === 'match' && matchResult && matchResult.status === 'error' && (
                  <ResultPanel>
                    <ResultTitle>Não foi possível buscar produtores</ResultTitle>
                    <HelperText style={{ color: '#EF4444' }}>{matchResult.message}</HelperText>
                  </ResultPanel>
                )}

                {modalStep === 'match' && matchResult && (!matchResult.opcoes || matchResult.opcoes.length === 0) && (
                  <ResultPanel>
                    <ResultTitle>Nenhum produtor retornado</ResultTitle>
                    <HelperText>
                      O motor de match não encontrou candidatos. Possíveis causas e próximos passos:
                    </HelperText>
                    <InfoList>
                      <InfoItem>Verifique se existe uma versão de demanda publicada para este edital.</InfoItem>
                      <InfoItem>Confirme se há produtores com itens compatíveis cadastrados e com endereço próximo.</InfoItem>
                      <InfoItem>Reenvie o PDF ou ajuste o catálogo de produtos para incluir equivalências.</InfoItem>
                    </InfoList>
                  </ResultPanel>
                )}
              </ModalBody>

              <ModalFooter>
                <FooterActions>
                  <SecondaryButton type="button" onClick={closeModal}>
                    Cancelar
                  </SecondaryButton>
                  {modalStep === 'input' && (
                    <SubmitButton type="button" onClick={uploadPdf} disabled={uploading}>
                      {uploading ? 'Processando...' : 'Processar edital'}
                    </SubmitButton>
                  )}
                  {modalStep === 'summary' && (
                    <SubmitButton type="button" onClick={goToMatchStep} disabled={!uploadResult}>
                      Ver recomendados
                    </SubmitButton>
                  )}
                  {modalStep === 'match' && (
                    <SubmitButton
                      type="button"
                      onClick={saveReport}
                      disabled={matchLoading || !matchResult || matchResult.status === 'pending'}
                    >
                      Salvar relatório
                    </SubmitButton>
                  )}
                </FooterActions>
              </ModalFooter>
            </ModalCard>
          </ModalOverlay>
        )}
      </MainContent>
    </Container>
  );
};

export default AdminDash;
