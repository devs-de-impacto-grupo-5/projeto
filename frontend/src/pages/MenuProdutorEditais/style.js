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
  align-items: flex-start;
  justify-content: space-between;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  border: 1px solid #e5e7eb;
  gap: 12px;
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
  background: rgba(106, 58, 159, 0.1);
  color: ${darkPurple};
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

export const ActionsRow = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

export const ApplyButton = styled.button`
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid ${darkPurple};
  background: ${darkPurple};
  color: #fff;
  font-weight: 800;
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 10px 20px rgba(106, 58, 159, 0.2);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

export const StatusText = styled.p`
  margin: 6px 0 0;
  font-size: 13px;
  font-weight: 700;
  color: ${darkPurple};
`;
