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
  ActionsRow,
  ApplyButton,
  StatusText,
} from './style';

const MenuProdutorEditais = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [statusMessage, setStatusMessage] = useState('');
  const [loadingApplyId, setLoadingApplyId] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        if (!token) {
          setError('Faça login para ver seus editais.');
          setLoading(false);
          return;
        }
        const resp = await fetch(`http://localhost:8084/demandas?status=published`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (resp.status === 401) {
          setError('Sessão expirada. Entre novamente.');
          setLoading(false);
          return;
        }
        if (!resp.ok) throw new Error('Não foi possível carregar os editais abertos.');
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

  const candidatar = async (demandaId) => {
    setStatusMessage('');
    const token = localStorage.getItem('access_token') || localStorage.getItem('token');
    const produtorId = localStorage.getItem('produtor_id') || localStorage.getItem('user_id');
    if (!token || !produtorId) {
      setStatusMessage('Faça login como produtor para se candidatar.');
      return;
    }
    try {
      setLoadingApplyId(demandaId);
      const detalheResp = await fetch(`http://localhost:8084/demandas/${demandaId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!detalheResp.ok) throw new Error('Não foi possível carregar o edital.');
      const detalhe = await detalheResp.json();
      const versaoId = detalhe.versao_atual_id || detalhe.versao_atual;
      if (!versaoId) throw new Error('Versão do edital não encontrada para candidatura.');

      const itens = (detalhe.itens || []).map((it) => ({
        item_demanda_id: it.id,
        produto_id: it.produto_id,
        unidade_id: it.unidade_id,
        quantidade: it.quantidade,
        preco: null,
        substituto_de_produto_id: null,
        motivo_substituicao: null,
        flag_aviso: false,
      }));

      const body = {
        versao_demanda_id: versaoId,
        organizacao_id: detalhe.organizacao_id || 0,
        tipo_proposta: 'single',
        produtor_id: Number(produtorId),
        valor_total: null,
        itens,
      };

      const propostaResp = await fetch('http://localhost:8084/propostas', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      if (!propostaResp.ok) {
        const errData = await propostaResp.json().catch(() => ({}));
        const msg = errData.detail || errData.erro || 'Não foi possível enviar sua candidatura.';
        throw new Error(msg);
      }

      setStatusMessage('Candidatura enviada! Acompanhe em Propostas.');
    } catch (err) {
      setStatusMessage(err.message);
    } finally {
      setLoadingApplyId(null);
    }
  };

  return (
    <Container>
      <Header>
        <div>
          <Title>Meus Editais</Title>
          <Subtitle>Editais abertos para participar.</Subtitle>
          {statusMessage && <StatusText>{statusMessage}</StatusText>}
        </div>
      </Header>

      {loading && <EmptyState>Carregando...</EmptyState>}
      {error && <EmptyState>{error}</EmptyState>}
      {!loading && !error && items.length === 0 && <EmptyState>Nenhum edital encontrado.</EmptyState>}

      <List>
        {items.map((item) => (
          <Card key={item.id}>
            <div>
              <CardTitle>{item.titulo || `Edital #${item.id}`}</CardTitle>
              <CardMeta>Status: {item.status || '—'} • Itens: {item.itens?.length || 0}</CardMeta>
            </div>
            <ActionsRow>
              <Badge>{item.status || 'aberto'}</Badge>
              <ApplyButton onClick={() => candidatar(item.id)} disabled={loadingApplyId === item.id}>
                {loadingApplyId === item.id ? 'Enviando...' : 'Quero participar'}
              </ApplyButton>
            </ActionsRow>
          </Card>
        ))}
      </List>
    </Container>
  );
};

export default MenuProdutorEditais;
