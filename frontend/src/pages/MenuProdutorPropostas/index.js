import { useEffect, useState } from 'react';
import {
  Container,
  Header,
  Title,
  Subtitle,
  List,
  Card,
  CardTitle,
  CardMeta,
  Badge,
  EmptyState,
} from './style';

const MenuProdutorPropostas = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        if (!token) {
          setError('Faça login para ver suas propostas.');
          setLoading(false);
          return;
        }
        const produtorId = localStorage.getItem('produtor_id') || localStorage.getItem('user_id');
        const resp = await fetch(`https://rj-devs-impacto-api.onrender.com/propostas?produtor_id=${produtorId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (resp.status === 401) {
          setError('Sessão expirada. Entre novamente.');
          setLoading(false);
          return;
        }
        if (!resp.ok) throw new Error('Não foi possível carregar as propostas.');
        const data = await resp.json();
        setItems(data || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <Container>
      <Header>
        <div>
          <Title>Propostas</Title>
          <Subtitle>Propostas enviadas ou recebidas.</Subtitle>
        </div>
      </Header>

      {loading && <EmptyState>Carregando...</EmptyState>}
      {error && <EmptyState>{error}</EmptyState>}
      {!loading && !error && items.length === 0 && <EmptyState>Nenhuma proposta encontrada.</EmptyState>}

      <List>
        {items.map((item) => (
          <Card key={item.id}>
            <div>
              <CardTitle>Proposta #{String(item.id).padStart(3, '0')}</CardTitle>
              <CardMeta>Status: {item.status}</CardMeta>
              <CardMeta>Versão da demanda: {item.versao_demanda_id}</CardMeta>
            </div>
            <Badge>{item.tipo_proposta === 'single' ? 'Individual' : 'Grupo'}</Badge>
          </Card>
        ))}
      </List>
    </Container>
  );
};

export default MenuProdutorPropostas;
