import React, { useState } from 'react';
import Modal from '../../components/Modal';
import { FormGroup, Label, Input, FormRow, Button, ErrorMessage, SuccessMessage } from './style';
import { FiCheck } from 'react-icons/fi';

const ModalAdicionarSafra = ({ isOpen, onClose, onSuccess, produtorId }) => {
  const [formData, setFormData] = useState({
    produto_nome: '',
    unidade_nome: '',
    quantidade: '',
    safra: new Date().getFullYear().toString(),
    preco_base: '',
    observacoes: '',
    ativo: true,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!formData.produto_nome || !formData.unidade_nome || !formData.quantidade) {
      setError('Preencha todos os campos obrigatórios');
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('token');
      const payload = {
        produtor_id: parseInt(produtorId, 10),
        produto_nome: formData.produto_nome.trim(),
        unidade_nome: formData.unidade_nome.trim(),
        preco_base: formData.preco_base ? parseFloat(formData.preco_base) : null,
        ativo: formData.ativo,
        quantidade: parseFloat(formData.quantidade),
        safra: formData.safra,
        observacoes: formData.observacoes || null,
      };

      const resp = await fetch('https://rj-devs-impacto-api.onrender.com/produtores/producao/manual', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!resp.ok) {
        const errorData = await resp.json();
        throw new Error(errorData.detail || 'Erro ao adicionar safra');
      }

      setSuccess('Safra adicionada com sucesso!');
      setFormData({
        produto_nome: '',
        unidade_nome: '',
        quantidade: '',
        safra: new Date().getFullYear().toString(),
        preco_base: '',
        observacoes: '',
        ativo: true,
      });

      setTimeout(() => {
        onSuccess();
        onClose();
      }, 1200);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const footer = (
    <>
      <Button type="button" variant="secondary" onClick={onClose} disabled={loading}>
        Cancelar
      </Button>
      <Button type="submit" variant="primary" onClick={handleSubmit} disabled={loading}>
        {loading ? 'Salvando...' : 'Adicionar Safra'}
      </Button>
    </>
  );

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Adicionar Safra" footer={footer}>
      <form onSubmit={handleSubmit}>
        {error && <ErrorMessage>{error}</ErrorMessage>}
        {success && (
          <SuccessMessage>
            <FiCheck size={16} /> {success}
          </SuccessMessage>
        )}

        <FormRow>
          <FormGroup>
            <Label>Produto (digite exatamente como deseja) *</Label>
            <Input
              type="text"
              name="produto_nome"
              value={formData.produto_nome}
              onChange={handleChange}
              placeholder="Ex: Tomate cereja orgânico"
              required
            />
          </FormGroup>
        </FormRow>

        <FormRow>
          <FormGroup>
            <Label>Unidade (ex: kg, caixa, maço) *</Label>
            <Input
              type="text"
              name="unidade_nome"
              value={formData.unidade_nome}
              onChange={handleChange}
              placeholder="Ex: kg"
              required
            />
          </FormGroup>
        </FormRow>

        <FormRow>
          <FormGroup>
            <Label>Quantidade *</Label>
            <Input
              type="number"
              name="quantidade"
              value={formData.quantidade}
              onChange={handleChange}
              placeholder="Ex: 100"
              step="0.01"
              required
            />
          </FormGroup>

          <FormGroup>
            <Label>Safra/Ano *</Label>
            <Input
              type="number"
              name="safra"
              value={formData.safra}
              onChange={handleChange}
              min="2000"
              max={new Date().getFullYear() + 1}
              required
            />
          </FormGroup>
        </FormRow>

        <FormRow>
          <FormGroup>
            <Label>Preço Base (Opcional)</Label>
            <Input
              type="number"
              name="preco_base"
              value={formData.preco_base}
              onChange={handleChange}
              placeholder="Ex: 10.50"
              step="0.01"
            />
          </FormGroup>
        </FormRow>

        <FormRow>
          <FormGroup>
            <Label>Observações</Label>
            <Input
              type="text"
              name="observacoes"
              value={formData.observacoes}
              onChange={handleChange}
              placeholder="Notas rápidas sobre a safra"
            />
          </FormGroup>
        </FormRow>

        <FormRow>
          <FormGroup>
            <Label>
              <input type="checkbox" name="ativo" checked={formData.ativo} onChange={handleChange} /> Ativo
            </Label>
          </FormGroup>
        </FormRow>
      </form>
    </Modal>
  );
};

export default ModalAdicionarSafra;
