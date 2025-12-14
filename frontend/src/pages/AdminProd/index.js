import React, { useState, useEffect, useMemo } from 'react';
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
  UserInfo,
  UserTitle,
  UserMeta,
  StatusBadge,
  ActionButton,
  DrawerOverlay,
  DrawerPanel,
  DrawerHeader,
  DrawerTitle,
  DrawerSub,
  DrawerContent,
  DrawerRow,
  DrawerLabel,
  DrawerValue,
  Tag,
  DrawerActions,
  PillButton,
  InsightCard,
  InsightTitle,
  InsightList,
  InsightItem,
  EmptyState,
  EmptyTitle,
  EmptyText,
  PaginationWrapper,
  PageButton,
  ResultsText,
} from './style';

import logoSvg from '../../assets/svgs/horizontal_logo.svg';
import personImage from '../../assets/png/assetPerson.png';
import {
  FiSearch,
  FiChevronLeft,
  FiChevronRight,
  FiEye,
  FiUsers,
  FiUserCheck,
  FiBriefcase,
} from 'react-icons/fi';

const AdminProd = () => {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [typeFilter, setTypeFilter] = useState('todos');
  const [currentPage, setCurrentPage] = useState(1);
  const [userName, setUserName] = useState('Usuário');
  const [selectedUser, setSelectedUser] = useState(null);
  const itemsPerPage = 10;

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

        const response = await fetch('http://localhost:8084/admin/usuarios', { headers });
        if (response.ok) {
          const data = await response.json();
          setUsers(data);
        }
      } catch (error) {
        console.error('Erro ao carregar usuários:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const stats = useMemo(() => {
    return {
      total: users.length,
      produtores: users.filter((u) => u.tipo_usuario === 'produtor').length,
      ativos: users.filter((u) => u.status === 'ativo').length,
    };
  }, [users]);

  const filteredUsers = useMemo(() => {
    let lista = [...users];

    if (typeFilter !== 'todos') {
      lista = lista.filter((item) => item.tipo_usuario === typeFilter);
    }

    if (searchTerm.trim()) {
      const termo = searchTerm.trim().toLowerCase();
      lista = lista.filter(
        (item) =>
          item.nome.toLowerCase().includes(termo) ||
          item.email.toLowerCase().includes(termo) ||
          String(item.id).includes(termo)
      );
    }

    return lista;
  }, [users, searchTerm, typeFilter]);

  const paginatedUsers = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return filteredUsers.slice(startIndex, startIndex + itemsPerPage);
  }, [filteredUsers, currentPage]);

  const totalPages = Math.ceil(filteredUsers.length / itemsPerPage);

  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  const statusLabel = (status) => {
    switch (status) {
      case 'ativo':
        return 'Ativo';
      case 'inativo':
        return 'Inativo';
      case 'pendente':
        return 'Pendente';
      default:
        return status || 'Desconhecido';
    }
  };

  const perfilLabel = (status) => {
    switch (status) {
      case 'complete':
        return 'Perfil completo';
      case 'incomplete':
        return 'Perfil incompleto';
      default:
        return status || 'Desconhecido';
    }
  };

  const typeLabel = (type) => {
    switch (type) {
      case 'produtor':
        return 'Produtor';
      case 'entidade_executora':
        return 'Entidade Executora';
      case 'admin':
        return 'Administrador';
      default:
        return type || 'Outro';
    }
  };

  const formatEndereco = (endereco) => {
    if (!endereco || typeof endereco !== 'object') return '—';
    const partes = [
      endereco.endereco,
      endereco.numero,
      endereco.cidade,
      endereco.uf,
    ].filter(Boolean);
    return partes.join(', ');
  };

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
            <NavItem to="/admin/prod" $active>
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
          <SectionBadge>Admin • Usuários</SectionBadge>
          <SectionMeta>Gerencie os produtores e entidades do sistema</SectionMeta>
        </TopBar>

        <ActionSection>
          <PageHeader>
            <PageTitle>Gestão de Produtores</PageTitle>
            <PageSubtitle>
              Visualize e gerencie todos os usuários cadastrados na plataforma.
            </PageSubtitle>
          </PageHeader>

          <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginLeft: 'auto' }}>
            <PillButton type="button">
              Exportar Detalhes
            </PillButton>
            <PillButton $primary type="button">
              Homologar resultado
            </PillButton>
          </div>
        </ActionSection>

        <StatsGrid>
          <StatCard $borderColor="#6B2E9E">
            <StatIconWrapper>
              <FiUsers size={22} />
            </StatIconWrapper>
            <StatInfo>
              <StatTitle>Total de Usuários</StatTitle>
              <StatValue>{loading ? '...' : stats.total}</StatValue>
            </StatInfo>
          </StatCard>

          <StatCard $borderColor="#27AE60">
            <StatIconWrapper>
              <FiBriefcase size={22} />
            </StatIconWrapper>
            <StatInfo>
              <StatTitle>Produtores</StatTitle>
              <StatValue>{loading ? '...' : stats.produtores}</StatValue>
            </StatInfo>
          </StatCard>

          <StatCard $borderColor="#2D9CDB">
            <StatIconWrapper>
              <FiUserCheck size={22} />
            </StatIconWrapper>
            <StatInfo>
              <StatTitle>Usuários Ativos</StatTitle>
              <StatValue>{loading ? '...' : stats.ativos}</StatValue>
            </StatInfo>
          </StatCard>
        </StatsGrid>

        <FiltersBar>
          <SearchInputWrapper>
            <FiSearch size={20} color="#A0A0A0" />
            <SearchInput
              placeholder="Buscar por nome, email ou ID"
              value={searchTerm}
              onChange={(e) => {
                setSearchTerm(e.target.value);
                setCurrentPage(1);
              }}
              aria-label="Buscar usuário"
            />
          </SearchInputWrapper>

          <FiltersRow>
            <FilterSelect
              value={typeFilter}
              onChange={(e) => {
                setTypeFilter(e.target.value);
                setCurrentPage(1);
              }}
              aria-label="Filtrar tipo"
            >
              <option value="todos">Todos os tipos</option>
              <option value="produtor">Produtor</option>
              <option value="entidade_executora">Entidade Executora</option>
              <option value="admin">Administrador</option>
            </FilterSelect>
          </FiltersRow>
        </FiltersBar>

        <TableCard>
          <TableContainer>
            <TableHeader>
              <div>ID</div>
              <div>Usuário</div>
              <div>Email</div>
              <div>Tipo</div>
              <div>Status</div>
              <div>Ações</div>
            </TableHeader>

            {loading ? (
              <div style={{ padding: '24px', textAlign: 'center', fontWeight: 700, color: '#4B5563' }}>
                Carregando dados...
              </div>
            ) : filteredUsers.length === 0 ? (
              <EmptyState>
                <EmptyTitle>Nenhum usuário encontrado</EmptyTitle>
                <EmptyText>
                  Tente ajustar os filtros de busca.
                </EmptyText>
              </EmptyState>
            ) : (
              paginatedUsers.map((user) => (
                <TableRow key={user.id}>
                  <IdBadge>{String(user.id).padStart(2, '0')}</IdBadge>

                  <UserInfo>
                    <UserTitle>{user.nome}</UserTitle>
                    <UserMeta>Cadastrado em: {new Date(user.created_at).toLocaleDateString('pt-BR')}</UserMeta>
                  </UserInfo>

                  <div style={{ fontSize: '13px', color: '#4B5563', fontWeight: 600 }}>
                    {user.email}
                  </div>

                  <div style={{ fontSize: '13px', color: '#111827', fontWeight: 700 }}>
                    {typeLabel(user.tipo_usuario)}
                  </div>

                  <StatusBadge $status={user.status}>{statusLabel(user.status)}</StatusBadge>

                  <ActionButton
                    type="button"
                    aria-label={`Visualizar usuário ${user.nome}`}
                    onClick={() => setSelectedUser(user)}
                  >
                    <FiEye size={18} />
                    Detalhes
                  </ActionButton>
                </TableRow>
              ))
            )}
          </TableContainer>

          <PaginationWrapper>
            <ResultsText>
              Mostrando <strong>{paginatedUsers.length}</strong> de <strong>{filteredUsers.length}</strong> resultados
            </ResultsText>
            <div style={{ display: 'flex', gap: '8px' }}>
              <PageButton 
                disabled={currentPage === 1}
                onClick={() => handlePageChange(currentPage - 1)}
              >
                <FiChevronLeft size={20} />
              </PageButton>
              
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                // Lógica simples de paginação para mostrar até 5 páginas
                let pageNum = i + 1;
                if (totalPages > 5 && currentPage > 3) {
                  pageNum = currentPage - 2 + i;
                  if (pageNum > totalPages) pageNum = totalPages - (4 - i);
                }
                
                return (
                  <PageButton 
                    key={pageNum} 
                    $active={currentPage === pageNum}
                    onClick={() => handlePageChange(pageNum)}
                  >
                    {pageNum}
                  </PageButton>
                );
              })}

              <PageButton 
                disabled={currentPage === totalPages || totalPages === 0}
                onClick={() => handlePageChange(currentPage + 1)}
              >
                <FiChevronRight size={20} />
              </PageButton>
            </div>
          </PaginationWrapper>
        </TableCard>

        {selectedUser && (
          <DrawerOverlay onClick={() => setSelectedUser(null)}>
            <DrawerPanel onClick={(e) => e.stopPropagation()}>
              <DrawerHeader>
                <div>
                  <DrawerTitle>{selectedUser.nome}</DrawerTitle>
                  <DrawerSub>
                    ID {selectedUser.id} • {typeLabel(selectedUser.tipo_usuario)}
                  </DrawerSub>
                </div>
                <Tag $tone={selectedUser.status}>{statusLabel(selectedUser.status)}</Tag>
              </DrawerHeader>

              <DrawerContent>
                <DrawerRow>
                  <DrawerLabel>Email</DrawerLabel>
                  <DrawerValue>{selectedUser.email}</DrawerValue>
                </DrawerRow>
                <DrawerRow>
                  <DrawerLabel>Tipo produtor</DrawerLabel>
                  <DrawerValue>{selectedUser.tipo_produtor || '—'}</DrawerValue>
                </DrawerRow>
                <DrawerRow>
                  <DrawerLabel>Cadastrado em</DrawerLabel>
                  <DrawerValue>
                    {selectedUser.created_at
                      ? new Date(selectedUser.created_at).toLocaleDateString('pt-BR')
                      : '---'}
                  </DrawerValue>
                </DrawerRow>
                <DrawerRow>
                  <DrawerLabel>Atualizado em</DrawerLabel>
                  <DrawerValue>
                    {selectedUser.updated_at
                      ? new Date(selectedUser.updated_at).toLocaleDateString('pt-BR')
                      : '---'}
                  </DrawerValue>
                </DrawerRow>
                <DrawerRow>
                  <DrawerLabel>Status</DrawerLabel>
                  <DrawerValue>{statusLabel(selectedUser.status)}</DrawerValue>
                </DrawerRow>
                <DrawerRow>
                  <DrawerLabel>Tipo</DrawerLabel>
                  <DrawerValue>{typeLabel(selectedUser.tipo_usuario)}</DrawerValue>
                </DrawerRow>
                <DrawerRow>
                  <DrawerLabel>Status do perfil</DrawerLabel>
                  <DrawerValue>{perfilLabel(selectedUser.status_perfil)}</DrawerValue>
                </DrawerRow>
                <DrawerRow>
                  <DrawerLabel>Identificação legal</DrawerLabel>
                  <DrawerValue>{selectedUser.identificacao_legal || '—'}</DrawerValue>
                </DrawerRow>
                <DrawerRow>
                  <DrawerLabel>RG / IE</DrawerLabel>
                  <DrawerValue>{selectedUser.rg_ie || '—'}</DrawerValue>
                </DrawerRow>
                <DrawerRow>
                  <DrawerLabel>Endereço</DrawerLabel>
                  <DrawerValue>{formatEndereco(selectedUser.endereco_json)}</DrawerValue>
                </DrawerRow>
                <DrawerRow>
                  <DrawerLabel>Capacidades</DrawerLabel>
                  <DrawerValue>
                    {selectedUser.capacidades_entrega_json
                      ? JSON.stringify(selectedUser.capacidades_entrega_json)
                      : '—'}
                  </DrawerValue>
                </DrawerRow>
              </DrawerContent>

              <InsightCard>
                <InsightTitle>Próximos passos para recomendação</InsightTitle>
                <InsightList>
                  <InsightItem>Confira endereço e certificações do produtor para aumentar o score.</InsightItem>
                  <InsightItem>Garanta produtos cadastrados no catálogo para aparecer nos matches.</InsightItem>
                  <InsightItem>Publique a versão do edital e rode o match para ver se ele é elegível.</InsightItem>
                </InsightList>
              </InsightCard>

              <DrawerActions>
                <PillButton type="button" onClick={() => setSelectedUser(null)}>
                  Fechar
                </PillButton>
                <PillButton
                  type="button"
                  $primary
                  onClick={() => {
                    localStorage.setItem('prefered_produtor_id', selectedUser.id);
                    navigate('/admin/dash');
                  }}
                >
                  Induzir recomendação no edital
                </PillButton>
              </DrawerActions>
            </DrawerPanel>
          </DrawerOverlay>
        )}
      </MainContent>
    </Container>
  );
};

export default AdminProd;
