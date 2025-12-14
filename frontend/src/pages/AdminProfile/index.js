import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
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
  ActionRow,
  ActionButton,
  ProfileCard,
  ProfileHeader,
  LargeAvatar,
  ProfileInfo,
  ProfileName,
  ProfileRole,
  StatusBadge,
  MetaRow,
  Tag,
  StatsGrid,
  StatCard,
  StatLabel,
  StatValue,
  InfoGrid,
  InfoGroup,
  Label,
  Value,
  InlineList,
} from './style';

import logoSvg from '../../assets/svgs/horizontal_logo.svg';
import personImage from '../../assets/png/assetPerson.png';

const AdminProfile = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [userName, setUserName] = useState('Usuário');

  useEffect(() => {
    const storedName = localStorage.getItem('user_name');
    const storedId = localStorage.getItem('user_id');

    if (storedName) {
      setUserName(storedName);
    }

    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token');
        const headers = {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        };

        const response = await fetch('http://localhost:8084/admin/usuarios', { headers });
        if (response.ok) {
          const users = await response.json();
          const currentUser = users.find((u) => String(u.id) === String(storedId));
          if (currentUser) {
            setUserData(currentUser);
          }
        }
      } catch (error) {
        console.error('Erro ao carregar dados do perfil:', error);
      } finally {
        setLoading(false);
      }
    };

    if (storedId) {
      fetchUserData();
    } else {
      setLoading(false);
    }
  }, []);

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const roleLabel = useMemo(() => {
    if (!userData) return '';
    if (userData.role === 'admin_master') return 'Admin Master';
    if (userData.role) return userData.role;
    return 'Administrador';
  }, [userData]);

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
            <NavItem to="/admin/prod">Produtores</NavItem>
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
          <SectionBadge>Admin • Perfil</SectionBadge>
          <SectionMeta>Visualize e gerencie as informações da sua conta.</SectionMeta>
        </TopBar>

        <PageHeader>
          <PageTitle>Meu Perfil</PageTitle>
          <ActionRow>
            <ActionButton type="button">Exportar dados</ActionButton>
            <ActionButton $primary type="button">Editar perfil</ActionButton>
          </ActionRow>
        </PageHeader>

        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: '#6B7280' }}>
            Carregando informações...
          </div>
        ) : userData ? (
          <ProfileCard>
            <ProfileHeader>
              <LargeAvatar src={personImage} alt={userData.nome} />
              <ProfileInfo>
                <ProfileName>{userData.nome}</ProfileName>
                <MetaRow>
                  <ProfileRole>{roleLabel}</ProfileRole>
                  <Tag>{userData.tipo_usuario?.replace('_', ' ') || 'Tipo indefinido'}</Tag>
                  <StatusBadge $active={userData.status === 'ativo'}>
                    {userData.status === 'ativo' ? 'Ativo' : 'Inativo'}
                  </StatusBadge>
                </MetaRow>
              </ProfileInfo>
            </ProfileHeader>

            <StatsGrid>
              <StatCard>
                <StatLabel>ID do usuário</StatLabel>
                <StatValue>#{String(userData.id).padStart(4, '0')}</StatValue>
              </StatCard>
              <StatCard>
                <StatLabel>Subtipo</StatLabel>
                <StatValue>{userData.subtipo_usuario || '-'}</StatValue>
              </StatCard>
              <StatCard>
                <StatLabel>Criado em</StatLabel>
                <StatValue>{formatDate(userData.created_at)}</StatValue>
              </StatCard>
              <StatCard>
                <StatLabel>Último login</StatLabel>
                <StatValue>{formatDate(userData.last_login_at)}</StatValue>
              </StatCard>
            </StatsGrid>

            <InfoGrid>
              <InfoGroup>
                <Label>Email</Label>
                <Value>{userData.email}</Value>
              </InfoGroup>

              <InfoGroup>
                <Label>Tipo de Usuário</Label>
                <Value style={{ textTransform: 'capitalize' }}>
                  {userData.tipo_usuario?.replace('_', ' ') || '-'}
                </Value>
              </InfoGroup>

              <InfoGroup>
                <Label>Função</Label>
                <Value>{roleLabel}</Value>
              </InfoGroup>

              <InfoGroup>
                <Label>Subtipo</Label>
                <Value style={{ textTransform: 'capitalize' }}>
                  {userData.subtipo_usuario?.replace('_', ' ') || '-'}
                </Value>
              </InfoGroup>

              <InfoGroup>
                <Label>Data de Cadastro</Label>
                <Value>{formatDate(userData.created_at)}</Value>
              </InfoGroup>

              <InfoGroup>
                <Label>Último Login</Label>
                <Value>{formatDate(userData.last_login_at)}</Value>
              </InfoGroup>

              <InfoGroup>
                <Label>Status</Label>
                <InlineList>
                  <Tag>{userData.status}</Tag>
                  <Tag>{userData.status_perfil || 'perfil desconhecido'}</Tag>
                </InlineList>
              </InfoGroup>
            </InfoGrid>
          </ProfileCard>
        ) : (
          <div style={{ padding: '40px', textAlign: 'center', color: '#6B7280' }}>
            Não foi possível carregar as informações do perfil.
          </div>
        )}
      </MainContent>
    </Container>
  );
};

export default AdminProfile;
