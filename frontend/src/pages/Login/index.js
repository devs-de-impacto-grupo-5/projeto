import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Chat from '../../components/Chat';
import { API_URL } from '../../constants/api_url';

const Login = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState('cpf'); // 'cpf', 'senha', 'cadastro_email', 'cadastro_nome', 'cadastro_senha', 'cadastro_subtipo'
  const [userData, setUserData] = useState({
    cpf: '',
    email: '',
    documento: '',
    name: '',
    senha: '',
    subtipo_usuario: '',
    latitude: null,
    longitude: null
  });

  const initialMessages = [
    { type: 'assistente', text: 'Olá! Seja bem-vindo(a) ao Vitalis! \n \n Por favor, para sua segurança, digite seu CPF.' }
  ];

  const formatCPF = (cpf) => {
    // Remove tudo que não é dígito
    const digits = cpf.replace(/\D/g, '');

    // Formata: XXX.XXX.XXX-XX
    return digits.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  };

  const validateCPF = (cpf) => {
    // Remove tudo que não é dígito
    const digits = cpf.replace(/\D/g, '');

    // Valida se tem exatamente 11 dígitos
    return digits.length === 11;
  };

  const getLocation = () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocalização não é suportada pelo seu navegador'));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          });
        },
        (error) => {
          reject(error);
        }
      );
    });
  };

  const handleRegister = async (setMessages, subtipo) => {
    // Adiciona indicador de "digitando"
    setMessages(prev => [...prev, { type: 'assistente', text: 'typing' }]);

    try {
      // Solicita localização
      let location;
      try {
        location = await getLocation();
        setUserData(prev => ({
          ...prev,
          latitude: location.latitude,
          longitude: location.longitude
        }));
      } catch (error) {
        console.error('Erro ao obter localização:', error);
        // Continua mesmo sem localização
        location = { latitude: null, longitude: null };
      }

      const response = await fetch(`${API_URL}register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cpf: userData.cpf,
          email: userData.email,
          latitude: location.latitude,
          longitude: location.longitude,
          name: userData.name,
          senha: userData.senha,
          subtipo_usuario: subtipo,
          tipo_usuario: 'produtor'
        }),
      });

      // Remove o indicador de "digitando"
      setMessages(prev => prev.filter(msg => msg.text !== 'typing'));

      if (response.ok) {
        const data = await response.json();
        setMessages(prev => [...prev, {
          type: 'assistente',
          text: `Cadastro realizado com sucesso, ${userData.name}! Fazendo login...`
        }]);

        // Faz login automático
        setTimeout(async () => {
          // Adiciona indicador de "digitando"
          setMessages(prev => [...prev, { type: 'assistente', text: 'typing' }]);

          try {
            const formData = new URLSearchParams();
            formData.append('grant_type', 'password');
            formData.append('username', userData.email);
            formData.append('password', userData.senha);
            formData.append('scope', '');
            formData.append('client_id', 'string');
            formData.append('client_secret', 'string');

            const loginResponse = await fetch('https://rj-devs-impacto-api.onrender.com/token', {
              method: 'POST',
              headers: {
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
              },
              body: formData.toString(),
            });

            const loginData = await loginResponse.json();

            // Remove o indicador de "digitando"
            setMessages(prev => prev.filter(msg => msg.text !== 'typing'));

            if (loginResponse.ok) {
              // Salva no localStorage
              localStorage.setItem('access_token', loginData.access_token);
              localStorage.setItem('role', loginData.role || '');
              localStorage.setItem('user_id', loginData.user_id);
              localStorage.setItem('user_name', loginData.name);
              localStorage.setItem('user_email', loginData.email);
              // Se vier do backend, usa. Senão usa do userData (caso do cadastro)
              localStorage.setItem('tipo_usuario', loginData.tipo_usuario || 'produtor');
              localStorage.setItem('subtipo_usuario', loginData.subtipo_usuario || userData.subtipo_usuario);

              setMessages(prev => [...prev, {
                type: 'assistente',
                text: `Bem-vindo, ${loginData.name}! Login realizado com sucesso.`
              }]);

              // Redireciona para a página de documentos
              setTimeout(() => {
                navigate('/documentos-produtor');
              }, 1500);
            } else {
              setMessages(prev => [...prev, {
                type: 'assistente',
                text: 'Cadastro realizado, mas houve um erro no login automático. Por favor, faça login manualmente.'
              }]);
            }
          } catch (error) {
            console.error('Erro no login automático:', error);
            setMessages(prev => prev.filter(msg => msg.text !== 'typing'));
            setMessages(prev => [...prev, {
              type: 'assistente',
              text: 'Cadastro realizado, mas houve um erro no login automático. Por favor, faça login manualmente.'
            }]);
          }
        }, 1000);
      } else {
        // Trata erro da API
        let errorMessage = 'Erro ao realizar cadastro. Por favor, tente novamente.';

        try {
          const errorData = await response.json();

          // Se o erro for um array de detalhes de validação
          if (Array.isArray(errorData.detail)) {
            errorMessage = errorData.detail.map(err => err.msg).join(', ');
          } else if (typeof errorData.detail === 'string') {
            errorMessage = errorData.detail;
          } else if (errorData.message) {
            errorMessage = errorData.message;
          }
        } catch (e) {
          console.error('Erro ao parsear resposta de erro:', e);
        }

        setMessages(prev => [...prev, {
          type: 'assistente',
          text: errorMessage
        }]);
      }
    } catch (error) {
      console.error('Erro ao registrar usuário:', error);

      // Remove o indicador de "digitando"
      setMessages(prev => prev.filter(msg => msg.text !== 'typing'));

      setMessages(prev => [...prev, {
        type: 'assistente',
        text: 'Ops! Ocorreu um erro ao realizar o cadastro. Por favor, tente novamente.'
      }]);
    }
  };

  const handleLogin = async (password, setMessages) => {
    // Adiciona indicador de "digitando"
    setMessages(prev => [...prev, { type: 'assistente', text: 'typing' }]);

    try {
      const formData = new URLSearchParams();
      formData.append('grant_type', 'password');
      formData.append('username', userData.email);
      formData.append('password', password);
      formData.append('scope', '');
      formData.append('client_id', 'string');
      formData.append('client_secret', 'string');

      const response = await fetch('https://rj-devs-impacto-api.onrender.com/token', {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });

      const data = await response.json();

      // Remove o indicador de "digitando"
      setMessages(prev => prev.filter(msg => msg.text !== 'typing'));

      if (response.ok) {
        // Salva no localStorage
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('role', data.role || '');
        localStorage.setItem('user_id', data.user_id);
        localStorage.setItem('user_name', data.name);
        localStorage.setItem('user_email', data.email);
        localStorage.setItem('tipo_usuario', data.tipo_usuario || '');
        localStorage.setItem('subtipo_usuario', data.subtipo_usuario || '');

        setMessages(prev => [...prev, {
          type: 'assistente',
          text: `Bem-vindo de volta, ${data.name}! Login realizado com sucesso.`
        }]);

        // Redireciona para a página de documentos
        setTimeout(() => {
          navigate('/documentos-produtor');
        }, 1500);
      } else {
        setMessages(prev => [...prev, {
          type: 'assistente',
          text: 'Senha incorreta. Por favor, tente novamente.'
        }]);
      }
    } catch (error) {
      console.error('Erro ao fazer login:', error);

      // Remove o indicador de "digitando"
      setMessages(prev => prev.filter(msg => msg.text !== 'typing'));

      setMessages(prev => [...prev, {
        type: 'assistente',
        text: 'Ops! Ocorreu um erro ao fazer login. Por favor, tente novamente.'
      }]);
    }
  };

  const handleSend = async (message, setMessages) => {
    if (step === 'cpf') {
      // Valida o CPF
      if (!validateCPF(message)) {
        setMessages(prev => [...prev, {
          type: 'assistente',
          text: 'CPF inválido! Por favor, digite um CPF com 11 dígitos.'
        }]);
        return;
      }

      // Formata o CPF
      const formattedCPF = formatCPF(message);

      // Adiciona indicador de "digitando"
      setMessages(prev => [...prev, { type: 'assistente', text: 'typing' }]);

      try {
        const response = await fetch(`${API_URL}validar-usuario`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ documento: formattedCPF }),
        });

        const data = await response.json();

        // Remove o indicador de "digitando"
        setMessages(prev => prev.filter(msg => msg.text !== 'typing'));

        // Armazena dados do usuário
        setUserData(prev => ({
          ...prev,
          cpf: formattedCPF,
          email: data.documento || '',
          documento: data.documento || ''
        }));

        // Adiciona a resposta baseada em ja_cadastrado
        if (data.ja_cadastrado) {
          setStep('senha');
          setUserData(prev => ({ ...prev, email: data.documento }));
          setMessages(prev => [...prev, {
            type: 'assistente',
            text: 'Vi aqui que você já é nosso usuário. Digite sua senha para continuar.'
          }]);
        } else {
          setStep('cadastro_email');
          setMessages(prev => [...prev, {
            type: 'assistente',
            text: 'Vi aqui que você não é nosso usuário. Vamos criar sua conta! Por favor, digite seu e-mail para continuarmos.'
          }]);
        }
      } catch (error) {
        console.error('Erro ao validar usuário:', error);

        // Remove o indicador de "digitando"
        setMessages(prev => prev.filter(msg => msg.text !== 'typing'));

        // Adiciona mensagem de erro
        setMessages(prev => [...prev, {
          type: 'assistente',
          text: 'Ops! Ocorreu um erro ao validar seu CPF. Por favor, tente novamente.'
        }]);
      }
    } else if (step === 'senha') {
      // Chama função de login
      await handleLogin(message, setMessages);
    } else if (step === 'cadastro_email') {
      // Salva email e pede nome
      setUserData(prev => ({ ...prev, email: message }));
      setStep('cadastro_nome');
      setMessages(prev => [...prev, {
        type: 'assistente',
        text: 'Ótimo! Agora me diga seu nome completo.'
      }]);
    } else if (step === 'cadastro_nome') {
      // Salva nome e pede senha
      setUserData(prev => ({ ...prev, name: message }));
      setStep('cadastro_senha');
      setMessages(prev => [...prev, {
        type: 'assistente',
        text: 'Perfeito! Agora crie uma senha para sua conta.'
      }]);
    } else if (step === 'cadastro_senha') {
      // Salva senha e pede subtipo
      setUserData(prev => ({ ...prev, senha: message }));
      setStep('cadastro_subtipo');
      setMessages(prev => [...prev, {
        type: 'assistente',
        text: 'Você vai se cadastrar como:\n\n1 - Fornecedor individual (sozinho)\n2 - Grupo informal\n3 - Grupo formal\n\nDigite o número da opção desejada.'
      }]);
    } else if (step === 'cadastro_subtipo') {
      // Define subtipo baseado na escolha
      let subtipo = '';
      if (message === '1') {
        subtipo = 'fornecedor_individual';
      } else if (message === '2') {
        subtipo = 'grupo_informal';
      } else if (message === '3') {
        subtipo = 'grupo_formal';
      } else {
        setMessages(prev => [...prev, {
          type: 'assistente',
          text: 'Opção inválida. Por favor, digite 1, 2 ou 3.'
        }]);
        return;
      }

      setUserData(prev => ({ ...prev, subtipo_usuario: subtipo }));

      // Finaliza cadastro passando subtipo diretamente
      await handleRegister(setMessages, subtipo);
    }
  };

  return (
    <Chat
      onBack={() => navigate('/')}
      onHelp={() => console.log('Help')}
      initialMessages={initialMessages}
      onSend={handleSend}
      inputType={step === 'senha' || step === 'cadastro_senha' ? 'password' : 'text'}
      placeholder="Digite aqui"
    />
  );
};

export default Login;
