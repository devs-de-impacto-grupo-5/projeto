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

const MenuProdutorNotificacoes = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        if (!token) {
          setError('Faça login para ver suas notificações.');
          setLoading(false);
          return;
        }
        const resp = await fetch(`https://rj-devs-impacto-api.onrender.com/notificacoes/minhas`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (resp.status === 401) {
          setError('Sessão expirada. Entre novamente.');
          setLoading(false);
          return;
        }
        if (!resp.ok) throw new Error('Não foi possível carregar as notificações.');
        const data = await resp.json();
        setItems((data && data.notificacoes) || []);
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
          <Title>Notificações</Title>
          <Subtitle>Alertas e comunicações importantes.</Subtitle>
        </div>
      </Header>

      {loading && <EmptyState>Carregando...</EmptyState>}
      {error && <EmptyState>{error}</EmptyState>}
      {!loading && !error && items.length === 0 && <EmptyState>Nenhuma notificação.</EmptyState>}

      <List>
        {items.map((item) => (
          <Card key={item.id}>
            <div>
              <CardTitle>{item.titulo || 'Notificação'}</CardTitle>
              <CardMeta>{item.mensagem || item.conteudo || 'Sem detalhes'}</CardMeta>
            </div>
            <Badge>{item.lida ? 'Lida' : 'Nova'}</Badge>
          </Card>
        ))}
      </List>
    </Container>
  );
};

export default MenuProdutorNotificacoes;
