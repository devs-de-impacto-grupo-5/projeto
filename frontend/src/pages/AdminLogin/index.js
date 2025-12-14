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
  InputGroup, 
  Label, 
  InputWrapper, 
  Input, 
  ForgotPasswordLink, 
  PrimaryButton, 
  Divider, 
  SecondaryButton,
  TopRightBlob,
  BottomLeftBlob
} from './style';
import logoSvg from '../../assets/svgs/horizontal_logo.svg';
import upperFormat from '../../assets/svgs/upperFormat.svg';
import downFormat from '../../assets/svgs/downFormat.svg';
import { FiUser, FiLock, FiEye, FiEyeOff } from 'react-icons/fi';

const AdminLogin = () => {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [emailOrCpf, setEmailOrCpf] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleLogin = async () => {
    if (!emailOrCpf || !password) {
      alert('Por favor, preencha todos os campos.');
      return;
    }

    setLoading(true);
    try {
      const formData = new URLSearchParams();
      formData.append('username', emailOrCpf);
      formData.append('password', password);

      const response = await fetch('http://localhost:8084/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro ao fazer login');
      }

      const data = await response.json();
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('role', data.role);
      localStorage.setItem('user', JSON.stringify(data));
      
      // Redirecionar para dashboard ou home
      navigate('/admin/dash'); 
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

      {/* Lado Direito (Formulário) */}
      <FormSection>
        <FormTitle>Entrar na minha conta</FormTitle>
        
        <InputGroup>
          <Label>E-mail ou CPF</Label>
          <InputWrapper>
            <FiUser color="#6B2E9E" size={20} />
            <Input 
              type="text" 
              placeholder="Digite seu e-mail ou CPF" 
              value={emailOrCpf}
              onChange={(e) => setEmailOrCpf(e.target.value)}
            />
          </InputWrapper>
        </InputGroup>

        <InputGroup>
          <Label>Senha</Label>
          <InputWrapper>
            <FiLock color="#6B2E9E" size={20} />
            <Input 
              type={showPassword ? "text" : "password"} 
              placeholder="Digite sua senha" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div onClick={togglePasswordVisibility} style={{ cursor: 'pointer', display: 'flex' }}>
              {showPassword ? (
                <FiEyeOff color="#A0A0A0" size={20} />
              ) : (
                <FiEye color="#A0A0A0" size={20} />
              )}
            </div>
          </InputWrapper>
        </InputGroup>

        <ForgotPasswordLink to="/forgot-password">Esqueci minha senha</ForgotPasswordLink>

        <PrimaryButton type="button" onClick={handleLogin} disabled={loading}>
          {loading ? 'Entrando...' : 'Entrar'}
        </PrimaryButton>
        
        <Divider>ou</Divider>
        
        <SecondaryButton to="/admin/register">Criar conta</SecondaryButton>
      </FormSection>
    </Container>
  );
};

export default AdminLogin;