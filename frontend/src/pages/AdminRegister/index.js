import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Container, 
  BannerSection, 
  FormSection, 
  LogoImage, 
  WelcomeTitle, 
  Slogan, 
  FormTitle, 
  FormSubtitle,
  InputGroup, 
  Label, 
  InputWrapper, 
  Input, 
  PrimaryButton, 
  Divider, 
  SecondaryButton 
} from './style';
import logoSvg from '../../assets/svgs/horizontal_logo.svg';
import { FiUser, FiLock, FiMail } from 'react-icons/fi';

const Register = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    cpf: '',
    password: '',
    confirmPassword: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleNextStep = () => {
    if (!formData.name || !formData.email || !formData.cpf) {
      alert('Preencha todos os campos');
      return;
    }
    setStep(2);
  };

  const handleFinalNext = () => {
    if (!formData.password || !formData.confirmPassword) {
      alert('Preencha todos os campos');
      return;
    }
    if (formData.password !== formData.confirmPassword) {
      alert('As senhas não coincidem');
      return;
    }
    // Navigate to address step with data
    navigate('/admin/address', { state: formData });
  };

  return (
    <Container>
      {/* Lado Esquerdo (Banner Roxo - Igual ao Login) */}
      <BannerSection>
        <LogoImage src={logoSvg} alt="Vitalis Logo" />
        <WelcomeTitle>Bem-vindo(a) ao Vitalis!</WelcomeTitle>
        <Slogan>Vital para quem produz, essencial para quem aprende</Slogan>
      </BannerSection>

      {/* Lado Direito (Formulário de Cadastro) */}
      <FormSection>
        <FormTitle>Criar uma conta</FormTitle>
        <FormSubtitle>
          {step === 1 ? 'Dados Pessoais' : 'Segurança'}
        </FormSubtitle>
        
        {step === 1 && (
          <>
            <InputGroup>
              <Label>Nome Completo</Label>
              <InputWrapper>
                <FiUser color="#6B2E9E" size={20} />
                <Input 
                  type="text" 
                  name="name"
                  placeholder="Digite seu nome completo" 
                  value={formData.name}
                  onChange={handleChange}
                />
              </InputWrapper>
            </InputGroup>

            <InputGroup>
              <Label>E-mail</Label>
              <InputWrapper>
                <FiMail color="#6B2E9E" size={20} />
                <Input 
                  type="email" 
                  name="email"
                  placeholder="Digite seu e-mail" 
                  value={formData.email}
                  onChange={handleChange}
                />
              </InputWrapper>
            </InputGroup>

            <InputGroup>
              <Label>CPF</Label>
              <InputWrapper>
                <FiUser color="#6B2E9E" size={20} />
                <Input 
                  type="text" 
                  name="cpf"
                  placeholder="Digite seu CPF" 
                  value={formData.cpf}
                  onChange={handleChange}
                />
              </InputWrapper>
            </InputGroup>

            <PrimaryButton type="button" onClick={handleNextStep}>Próximo</PrimaryButton>
          </>
        )}

        {step === 2 && (
          <>
            <InputGroup>
              <Label>Senha</Label>
              <InputWrapper>
                <FiLock color="#6B2E9E" size={20} />
                <Input 
                  type="password" 
                  name="password"
                  placeholder="Digite sua senha" 
                  value={formData.password}
                  onChange={handleChange}
                />
              </InputWrapper>
            </InputGroup>

            <InputGroup>
              <Label>Confirme a senha</Label>
              <InputWrapper>
                <FiLock color="#6B2E9E" size={20} />
                <Input 
                  type="password" 
                  name="confirmPassword"
                  placeholder="Confirme sua senha" 
                  value={formData.confirmPassword}
                  onChange={handleChange}
                />
              </InputWrapper>
            </InputGroup>

            <PrimaryButton type="button" onClick={handleFinalNext}>Próximo</PrimaryButton>
            
            <div style={{ width: '100%', marginTop: '10px' }}>
              <SecondaryButton as="button" onClick={() => setStep(1)} style={{ cursor: 'pointer' }}>
                Voltar
              </SecondaryButton>
            </div>
          </>
        )}
        
        <Divider>ou</Divider>
        
        {/* Botão Entrar (Outline) - Redireciona para login */}
        <SecondaryButton to="/admin/login">Entrar</SecondaryButton>
      </FormSection>
    </Container>
  );
};

export default Register;