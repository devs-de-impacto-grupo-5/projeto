import React, { useEffect, useMemo, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
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
  Hero,
  MetaRow,
  MetaLabel,
  MetaValue,
  PageTitle,
  PageSubtitle,
  Actions,
  PrimaryButton,
  GhostButton,
  StatsGrid,
  StatCard,
  StatIcon,
  StatLabel,
  StatValue,
  SectionCard,
  SectionHeader,
  SectionTitle,
  SectionSubtitle,
  ItemList,
  ItemRow,
  ItemName,
  ItemMeta,
  ProgressBar,
  ProgressFill,
  CandidateSection,
  CandidateHeaderRow,
  CandidateRow,
  CandidateCell,
  CandidateName,
  CandidateInfo,
  CandidateTag,
  StatusBadge,
  PillButton,
  EmptyState,
  EmptyTitle,
  EmptyText,
} from './style';

import logoSvg from '../../assets/svgs/horizontal_logo.svg';
import personImage from '../../assets/png/assetPerson.png';
import { FiDownload, FiCheckCircle, FiPieChart, FiUsers, FiPackage } from 'react-icons/fi';
import { BsStars } from 'react-icons/bs';

const EditalDetail = () => {
  const { id } = useParams();
  const [demanda, setDemanda] = useState(null);
  const [propostas, setPropostas] = useState([]);
  const [loading, setLoading] = useState(true);
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

        const demandaResponse = await fetch(`https://rj-devs-impacto-api.onrender.com/demandas/${id}`, { headers });
        if (demandaResponse.ok) {
          const demandaData = await demandaResponse.json();
          setDemanda(demandaData);

          if (demandaData.versao_atual_id) {
            const propostasResponse = await fetch(
              `https://rj-devs-impacto-api.onrender.com/propostas?versao_demanda_id=${demandaData.versao_atual_id}`,
              { headers },
            );
            if (propostasResponse.ok) {
              const propostasData = await propostasResponse.json();
              setPropostas(propostasData);
            }
          }
        }
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const formatDate = (dateString) => {
    const options = { day: 'numeric', month: 'short', year: 'numeric' };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
  };

  const statusLabel = (status) => {
    if (!status) return 'Indefinido';
    if (status === 'published' || status === 'ativo') return 'Ativo';
    if (status === 'draft') return 'Rascunho';
    if (status === 'encerrado') return 'Encerrado';
    return status;
  };

  const statusTone = (status) => {
    if (status === 'published' || status === 'ativo') return 'success';
    if (status === 'encerrado') return 'error';
    return 'neutral';
  };

  const metrics = useMemo(() => {
    const itens = demanda?.itens || [];
    return [
      {
        icon: <FiPackage />,
        label: 'Itens no edital',
        value: itens.length,
      },
      {
        icon: <FiUsers />,
        label: 'Candidatos',
        value: propostas.length,
      },
      {
        icon: <FiPieChart />,
        label: 'Status',
        value: statusLabel(demanda?.status),
      },
      {
        icon: <BsStars />,
        label: 'Atualizado',
        value: demanda?.created_at ? formatDate(demanda.created_at) : '--',
      },
    ];
  }, [demanda, propostas]);

  const handleExportDetails = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`https://rj-devs-impacto-api.onrender.com/admin/editais/${id}/download`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `edital_${id}_detalhes.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        console.error('Erro ao baixar detalhes');
      }
    } catch (error) {
      console.error('Erro na requisição:', error);
    }
  };

  if (loading) return <div style={{ padding: 20 }}>Carregando...</div>;
  if (!demanda) return <div style={{ padding: 20 }}>Demanda não encontrada</div>;

  return (
    <Container>
      <Header>
        <HeaderContent>
          <Link to="/admin/dash">
            <LogoImage src={logoSvg} alt="Vitalis" />
          </Link>

          <NavMenu aria-label="Navegação principal">
            <NavItem to="/admin/dash">Início</NavItem>
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
          <SectionBadge>Admin • Edital</SectionBadge>
          <SectionMeta>Revisão e acompanhamento do edital {`#${String(demanda.id).padStart(2, '0')}`}</SectionMeta>
        </TopBar>

        <Hero>
          <div>
            <MetaRow>
              <StatusBadge $tone={statusTone(demanda.status)}>{statusLabel(demanda.status)}</StatusBadge>
              <MetaValue>Publicado em {demanda.created_at ? formatDate(demanda.created_at) : '--'}</MetaValue>
            </MetaRow>

            <PageTitle>
              Edital #{String(demanda.id).padStart(2, '0')}: {demanda.titulo}
            </PageTitle>
            <PageSubtitle>
              {demanda.descricao || 'Sem descrição disponível para este edital.'}
            </PageSubtitle>
          </div>

          <Actions>
            <GhostButton type="button" onClick={handleExportDetails}>
              <FiDownload size={18} />
              Exportar Detalhes
            </GhostButton>
            <PrimaryButton type="button">
              <FiCheckCircle size={18} />
              Homologar resultado
            </PrimaryButton>
          </Actions>
        </Hero>

        <StatsGrid>
          {metrics.map((metric) => (
            <StatCard key={metric.label}>
              <StatIcon>{metric.icon}</StatIcon>
              <div>
                <StatLabel>{metric.label}</StatLabel>
                <StatValue>{metric.value ?? '--'}</StatValue>
              </div>
            </StatCard>
          ))}
        </StatsGrid>

        <SectionCard>
          <SectionHeader>
            <div>
              <SectionTitle>Itens do edital</SectionTitle>
              <SectionSubtitle>Detalhamento do que precisa ser atendido.</SectionSubtitle>
            </div>
            <SectionMeta>Última atualização {demanda.updated_at ? formatDate(demanda.updated_at) : '--'}</SectionMeta>
          </SectionHeader>

          <ItemList>
            {(demanda.itens || []).map((item) => (
              <ItemRow key={item.id}>
                <div>
                  <ItemName>{item.produto_nome}</ItemName>
                  <ItemMeta>
                    Quantidade: <strong>{item.quantidade}</strong> {item.unidade_nome}
                  </ItemMeta>
                </div>
                <div>
                  <MetaLabel>Atendido</MetaLabel>
                  <ProgressBar>
                    <ProgressFill style={{ width: '0%' }} />
                  </ProgressBar>
                  <MetaValue>0%</MetaValue>
                </div>
              </ItemRow>
            ))}
          </ItemList>
        </SectionCard>

        <CandidateSection>
          <SectionHeader>
            <div>
              <SectionTitle>Candidatos</SectionTitle>
              <SectionSubtitle>Produtores e propostas para este edital.</SectionSubtitle>
            </div>
            <Actions>
              <GhostButton type="button">Ordenar</GhostButton>
              <GhostButton type="button">Filtrar</GhostButton>
            </Actions>
          </SectionHeader>

          <CandidateHeaderRow>
            <CandidateCell $muted>Produtor</CandidateCell>
            <CandidateCell $muted>Itens</CandidateCell>
            <CandidateCell $muted>Valor total</CandidateCell>
            <CandidateCell $muted>Status</CandidateCell>
            <CandidateCell $muted align="right">
              Ação
            </CandidateCell>
          </CandidateHeaderRow>

          {propostas.length === 0 ? (
            <EmptyState>
              <EmptyTitle>Nenhum candidato</EmptyTitle>
              <EmptyText>Ainda não há propostas para este edital.</EmptyText>
            </EmptyState>
          ) : (
            propostas.map((proposta) => (
              <CandidateRow key={proposta.id}>
                <CandidateCell>
                  <CandidateInfo>
                    <CandidateName>{proposta.produtor_nome || `Produtor #${proposta.produtor_id}`}</CandidateName>
                    <CandidateTag>Produtor individual</CandidateTag>
                  </CandidateInfo>
                </CandidateCell>

                <CandidateCell>
                  <CandidateTag>{proposta.itens.length} itens</CandidateTag>
                </CandidateCell>

                <CandidateCell>
                  {proposta.valor_total ? `R$ ${parseFloat(proposta.valor_total).toFixed(2)}` : '—'}
                </CandidateCell>

                <CandidateCell>
                  <StatusBadge $tone={statusTone(proposta.status)}>
                    {statusLabel(proposta.status)}
                  </StatusBadge>
                </CandidateCell>

                <CandidateCell align="right">
                  <PillButton type="button">Ver proposta</PillButton>
                </CandidateCell>
              </CandidateRow>
            ))
          )}
        </CandidateSection>
      </MainContent>
    </Container>
  );
};

export default EditalDetail;
