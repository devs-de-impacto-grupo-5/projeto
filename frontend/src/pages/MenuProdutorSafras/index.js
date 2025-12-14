import { useEffect, useState } from 'react';
import { FiPackage, FiCalendar, FiDollarSign, FiPlus } from 'react-icons/fi';
import { PiPlantFill } from 'react-icons/pi';
import {
  Container,
  Header,
  Title,
  Subtitle,
  List,
  Card,
  CardContent,
  CardTitle,
  CardMeta,
  MetaRow,
  Badge,
  EmptyState,
  EmptyText,
  EmptyIcon,
  Footer,
  AddButton,
  PriceTag,
} from './style';
import ModalAdicionarSafra from '../../components/ModalAdicionarSafra';

const MenuProdutorSafras = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const produtorId = localStorage.getItem('produtor_id') || localStorage.getItem('user_id');

  const carregarSafras = async () => {
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('token');
      if (!token) {
        setError('Faça login para ver suas safras.');
        setLoading(false);
        return;
      }
      const resp = await fetch(`https://rj-devs-impacto-api.onrender.com/produtores/producao/${produtorId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (resp.status === 401) {
        setError('Sessão expirada. Entre novamente.');
        setLoading(false);
        return;
      }
      if (!resp.ok) throw new Error('Não foi possível carregar as safras.');
      const data = await resp.json();
      setItems(data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarSafras();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [produtorId]);

  const handleAddSafra = () => {
    carregarSafras();
  };

  return (
    <Container>
      <Header>
        <div>
          <Title>Minhas Safras</Title>
          <Subtitle>Acompanhe sua produção cadastrada e capacidade declarada.</Subtitle>
        </div>
      </Header>

      {loading && (
        <EmptyState>
          <EmptyIcon>⏳</EmptyIcon>
          <EmptyText>Carregando suas safras...</EmptyText>
        </EmptyState>
      )}
      
      {error && (
        <EmptyState>
          <EmptyIcon>⚠️</EmptyIcon>
          <EmptyText>{error}</EmptyText>
        </EmptyState>
      )}
      
      {!loading && !error && items.length === 0 && (
        <EmptyState>
          <EmptyIcon>
            <PiPlantFill />
          </EmptyIcon>
          <EmptyText>Você ainda não cadastrou safras.</EmptyText>
          <EmptyText style={{ fontSize: '13px', marginTop: '4px', opacity: 0.7 }}>
            Clique em "Adicionar Safra" para começar.
          </EmptyText>
        </EmptyState>
      )}

      <List>
        {items.map((item) => (
          <Card key={item.id}>
            <CardContent>
              <CardTitle>
                <PiPlantFill size={22} />
                {item.produto_nome || 'Produto sem nome'}
              </CardTitle>
              <CardMeta>
                <MetaRow>
                  <FiPackage size={16} />
                  <strong>Quantidade:</strong> {item.quantidade || '-'} {item.unidade_nome || ''}
                </MetaRow>
                <MetaRow>
                  <FiCalendar size={16} />
                  <strong>Safra:</strong> {item.safra || '--'}
                </MetaRow>
                {item.preco_base && (
                  <MetaRow>
                    <FiDollarSign size={16} />
                    <PriceTag>R$ {Number(item.preco_base).toFixed(2)}</PriceTag>
                  </MetaRow>
                )}
              </CardMeta>
            </CardContent>
            <Badge $active={item.ativo}>
              {item.ativo ? '✓ Ativo' : '✕ Inativo'}
            </Badge>
          </Card>
        ))}
      </List>

      <Footer>
        <AddButton onClick={() => setModalOpen(true)}>
          <FiPlus size={20} />
          Adicionar Safra
        </AddButton>
      </Footer>

      <ModalAdicionarSafra
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        onSuccess={handleAddSafra}
        produtorId={produtorId}
      />
    </Container>
  );
};

export default MenuProdutorSafras;
