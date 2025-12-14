import styled from 'styled-components';
import { darkPurple } from '../../constants/colors';
const muted = '#6B7280';

export const Container = styled.div`
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fb 0%, #ffffff 100%);
  box-sizing: border-box;
`;

export const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
`;

export const Title = styled.h1`
  margin: 0;
  font-size: 22px;
  font-weight: 900;
  color: ${darkPurple};
`;

export const Subtitle = styled.p`
  margin: 4px 0 0;
  font-size: 14px;
  color: ${muted};
  font-weight: 600;
`;

export const List = styled.div`
  display: grid;
  gap: 12px;
`;

export const Card = styled.div`
  background: white;
  border-radius: 16px;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  border: 1px solid #e5e7eb;
`;

export const CardTitle = styled.h3`
  margin: 0;
  font-size: 16px;
  font-weight: 800;
  color: ${darkPurple};
`;

export const CardMeta = styled.div`
  margin-top: 4px;
  font-size: 13px;
  color: ${muted};
  font-weight: 600;
`;

export const Badge = styled.span`
  padding: 8px 10px;
  border-radius: 12px;
  background: ${(p) => (p.children === 'Nova' ? 'rgba(22, 163, 74, 0.12)' : 'rgba(107, 114, 128, 0.12)')};
  color: ${(p) => (p.children === 'Nova' ? '#0f766e' : '#4b5563')};
  font-weight: 800;
  font-size: 12px;
`;

export const EmptyState = styled.div`
  background: white;
  border-radius: 14px;
  padding: 18px;
  text-align: center;
  color: ${muted};
  font-weight: 700;
  border: 1px solid #e5e7eb;
`;
