import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
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

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/inicio" element={<Inicio />} />
        <Route path="/inicio" element={<Inicio />} />
        <Route path="/login" element={<Login />} />
        <Route path="/documentos-produtor" element={<Documentos />} />
        <Route path="/enviar-documento" element={<EnviarDocumentoChat />} />
        <Route path="/menu-produtor" element={<MenuProdutor />} />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin/register" element={<AdminRegister />} />
        <Route path="/admin/address" element={<AdminAddress />} />
        <Route path="/admin/dash" element={<AdminDash />} />
        <Route path="/admin/edit/:id" element={<AdminEdit />} />
        <Route path="/admin/prod" element={<AdminProd />} />
        <Route path="/admin/profile" element={<AdminProfile />} />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin/register" element={<AdminRegister />} />
        <Route path="/admin/address" element={<AdminAddress />} />
        <Route path="/admin/dash" element={<AdminDash />} />
        <Route path="/admin/edit/:id" element={<AdminEdit />} />
        <Route path="/admin/prod" element={<AdminProd />} />
        <Route path="/admin/profile" element={<AdminProfile />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
