import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from '../pages/Home';
import Login from '../pages/Login';
import Documentos from '../pages/Documentos';
import MenuProdutor from '../pages/MenuProdutor';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/documentos-produtor" element={<Documentos />} />
        <Route path="/menu-produtor" element={<MenuProdutor />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
