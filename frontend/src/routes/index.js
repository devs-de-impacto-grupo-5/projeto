import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from '../pages/Home';
import Login from '../pages/Login';
import Documentos from '../pages/Documentos';
import MenuProdutor from '../pages/MenuProdutor';
import EnviarDocumentoChat from '../pages/EnviarDocumentoChat';
import Inicio from '../pages/Inicio';
import AdminLogin from '../pages/AdminLogin';
import AdminAddress from '../pages/AdminAddress';
import AdminDash from '../pages/AdminDash';
import AdminEdit from '../pages/AdminEdit';
import AdminProd from '../pages/AdminProd';
import AdminRegister from '../pages/AdminRegister';
import AdminProfile from '../pages/AdminProfile';
import MenuProdutorSafras from '../pages/MenuProdutorSafras';
import MenuProdutorEditais from '../pages/MenuProdutorEditais';
import MenuProdutorPropostas from '../pages/MenuProdutorPropostas';
import MenuProdutorNotificacoes from '../pages/MenuProdutorNotificacoes';

const InicioProdutor = () => {
  const nome = localStorage.getItem('user_name');
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return `Bom dia,`;
    if (hour < 18) return `Boa tarde,`;
    return `Boa noite,`;
  };

  return (
    <div>
      <div style={{ padding: '20px', backgroundColor: '#f0f0f0' }}>
        <h2>{getGreeting()}</h2>
        {nome && <p>{nome}</p>}
      </div>
      <Inicio />
    </div>
  );
};

const AppRoutes = () => {
  const AdminRoute = ({ element }) => {
    const role = localStorage.getItem('role');
    const tipoUsuario = localStorage.getItem('tipo_usuario');

    if (tipoUsuario === 'produtor') {
      return <Navigate to="/menu-produtor" replace />;
    }

    if (role == 'admin') {
      return <Navigate to="/admin/login" replace />;
    }

    return element;
  };

  const ProdutorRoute = ({ element }) => {
    const tipoUsuario = localStorage.getItem('tipo_usuario');
    if (tipoUsuario === 'produtor') {
      return <Navigate to="/inicio-produtor" replace />;
    }
    return element;
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/inicio" element={<ProdutorRoute element={<Inicio />} />} />
        <Route path="/inicio-produtor" element={<InicioProdutor />} />
        <Route path="/login" element={<Login />} />
        <Route path="/documentos-produtor" element={<Documentos />} />
        <Route path="/enviar-documento" element={<EnviarDocumentoChat />} />
        <Route path="/menu-produtor" element={<MenuProdutor />} />
        <Route path="/menu-produtor/safras" element={<MenuProdutorSafras />} />
        <Route path="/menu-produtor/editais" element={<MenuProdutorEditais />} />
        <Route path="/menu-produtor/propostas" element={<MenuProdutorPropostas />} />
        <Route path="/menu-produtor/notificacoes" element={<MenuProdutorNotificacoes />} />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin/register" element={<AdminRegister />} />
        <Route path="/admin/address" element={<AdminAddress />} />
        <Route path="/admin/dash" element={<AdminRoute element={<AdminDash />} />} />
        <Route path="/admin/edit/:id" element={<AdminRoute element={<AdminEdit />} />} />
        <Route path="/admin/prod" element={<AdminRoute element={<AdminProd />} />} />
        <Route path="/admin/profile" element={<AdminRoute element={<AdminProfile />} />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
