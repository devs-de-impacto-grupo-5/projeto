import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  Container, 
  BannerSection, 
  FormSection, 
  LogoImage, 
  WelcomeTitle, 
  Slogan, 
  FormTitle, 
  FormSubtitle,
  FormRow,
  InputGroup, 
  Label, 
  InputWrapper, 
  Input, 
  Select,
  PersonAvatar,
  PrimaryButton, 
  Divider, 
  SecondaryButton,
  TopRightBlob,
  BottomLeftBlob
} from './style';
import logoSvg from '../../assets/svgs/horizontal_logo.svg';
import upperFormat from '../../assets/svgs/upperFormat.svg';
import downFormat from '../../assets/svgs/downFormat.svg';
import personImage from '../../assets/png/assetPerson.png';
import { FiMapPin, FiMap } from 'react-icons/fi';
import { BiBuilding } from 'react-icons/bi';
import { TbNumbers } from 'react-icons/tb';

const RegisterAddress = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const prevData = location.state || {};

  const [addressData, setAddressData] = useState({
    uf: '',
    cidade: '',
    endereco: '',
    numero: ''
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setAddressData({ ...addressData, [e.target.name]: e.target.value });
  };

  const handleRegister = async () => {
    if (!prevData.name) {
      alert('Dados de cadastro ausentes. Volte para a etapa anterior.');
      navigate('/admin/register');
      return;
    }
    if (!addressData.uf || !addressData.cidade || !addressData.endereco || !addressData.numero) {
      alert('Preencha todos os campos de endereço');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        tipo_usuario: "produtor",
        subtipo_usuario: "fornecedor_individual",
        name: prevData.name,
        email: prevData.email,
        senha: prevData.password,
        cpf: prevData.cpf,
        endereco: addressData.endereco,
        numero: addressData.numero,
        cidade: addressData.cidade,
        uf: addressData.uf,
        latitude: 0, 
        longitude: 0
      };

      // FastAPI is mounted with root_path "/api/auth"
      const response = await fetch('http://localhost:8084/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        let errorMessage = 'Erro ao registrar';
        try {
          const errorData = await response.json();
          if (errorData?.detail) errorMessage = errorData.detail;
        } catch (_err) {
          // ignore JSON parse errors and use default message
        }
        throw new Error(errorMessage);
      }

      alert('Cadastro realizado com sucesso!');
      navigate('/admin/login');
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <TopRightBlob src={upperFormat} alt="" />
      <BottomLeftBlob src={downFormat} alt="" />
      
      <BannerSection>
        <LogoImage src={logoSvg} alt="Vitalis Logo" />
        <WelcomeTitle>Bem-vindo(a) ao Vitalis!</WelcomeTitle>
        <Slogan>Vital para quem produz, essencial para quem aprende</Slogan>
      </BannerSection>

      {/* Lado Direito (Formulário de Endereço) */}
      <FormSection>
        <FormTitle>Criar uma conta</FormTitle>
        <FormSubtitle>Última etapa antes de acessar!</FormSubtitle>
        
        {/* Linha com UF e Cidade */}
        <FormRow>
          <InputGroup style={{ flex: '0 0 100px' }}> {/* UF ocupa menos espaço */}
            <Label>UF</Label>
            <InputWrapper>
              <FiMapPin color="#6B2E9E" size={20} />
              <Select 
                name="uf" 
                value={addressData.uf} 
                onChange={handleChange}
              >
                <option value="" disabled hidden>UF</option>
                <option value="SP">SP</option>
                <option value="RJ">RJ</option>
                <option value="MG">MG</option>
              </Select>
            </InputWrapper>
          </InputGroup>

          <InputGroup style={{ flex: 1 }}> {/* Cidade ocupa o resto */}
            <Label>Cidade</Label>
            <InputWrapper>
              <BiBuilding color="#6B2E9E" size={20} />
              <Select 
                name="cidade" 
                value={addressData.cidade} 
                onChange={handleChange}
              >
                <option value="" disabled hidden>Selecione a cidade</option>
                <option value="saopaulo">São Paulo</option>
                <option value="rio">Rio de Janeiro</option>
              </Select>
            </InputWrapper>
          </InputGroup>

          <PersonAvatar src={personImage} alt="Avatar" />
        </FormRow>

        <InputGroup>
          <Label>Endereço</Label>
          <InputWrapper>
            <FiMap color="#6B2E9E" size={20} />
            <Input 
              type="text" 
              name="endereco"
              placeholder="Digite o endereço (rua e bairro)" 
              value={addressData.endereco}
              onChange={handleChange}
            />
          </InputWrapper>
        </InputGroup>

        <InputGroup>
          <Label>Número/Complemento</Label>
          <InputWrapper>
            <TbNumbers color="#6B2E9E" size={22} />
            <Input 
              type="text" 
              name="numero"
              placeholder="Digite o número e/ou complemento" 
              value={addressData.numero}
              onChange={handleChange}
            />
          </InputWrapper>
        </InputGroup>

        <PrimaryButton type="button" onClick={handleRegister} disabled={loading}>
          {loading ? 'Cadastrando...' : 'Finalizar'}
        </PrimaryButton>
        
        <Divider>ou</Divider>
        
        <SecondaryButton to="/admin/login">Entrar</SecondaryButton>
      </FormSection>
    </Container>
  );
};

export default RegisterAddress;
