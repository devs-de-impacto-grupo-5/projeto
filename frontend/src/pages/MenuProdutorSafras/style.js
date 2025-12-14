import styled from 'styled-components';
import { darkPurple } from '../../constants/colors';
const muted = '#6B7280';

export const Container = styled.div`
  min-height: 100vh;
  padding: 32px 20px 120px;
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 50%, #e5e7eb 100%);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 20px;

  @media (max-width: 768px) {
    padding: 24px 16px 100px;
    gap: 16px;
  }

  @media (max-width: 480px) {
    padding: 20px 12px 90px;
    gap: 12px;
  }
`;

export const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  width: 100%;
  max-width: 1040px;

  @media (max-width: 768px) {
    margin-bottom: 16px;
  }

  @media (max-width: 480px) {
    margin-bottom: 12px;
  }
`;

export const Title = styled.h1`
  margin: 0;
  font-size: 32px;
  font-weight: 900;
  color: ${darkPurple};
  letter-spacing: -0.5px;

  @media (max-width: 768px) {
    font-size: 28px;
  }

  @media (max-width: 480px) {
    font-size: 24px;
    letter-spacing: -0.3px;
  }
`;

export const Subtitle = styled.p`
  margin: 8px 0 0;
  font-size: 15px;
  color: ${muted};
  font-weight: 600;
  line-height: 1.5;

  @media (max-width: 768px) {
    font-size: 14px;
    margin: 6px 0 0;
  }

  @media (max-width: 480px) {
    font-size: 13px;
    margin: 4px 0 0;
  }
`;

export const List = styled.div`
  width: 100%;
  max-width: 1040px;
  display: flex;
  flex-direction: column;
  gap: 20px;

  @media (max-width: 768px) {
    gap: 16px;
  }

  @media (max-width: 480px) {
    gap: 12px;
  }
`;

export const Card = styled.div`
  background: white;
  border-radius: 20px;
  padding: 24px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.08);
  border: 1px solid #f3f4f6;
  gap: 16px;
  width: 100%;
  transition: all 0.3s ease;
  cursor: pointer;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(107, 46, 158, 0.15);
    border-color: ${darkPurple};
  }

  @media (max-width: 768px) {
    padding: 20px;
    border-radius: 16px;
    gap: 12px;
  }

  @media (max-width: 480px) {
    padding: 16px;
    border-radius: 14px;
    flex-direction: column;
    gap: 12px;

    &:hover {
      transform: translateY(-2px);
    }
  }
`;

export const CardContent = styled.div`
  flex: 1;

  @media (max-width: 480px) {
    width: 100%;
  }
`;

export const CardTitle = styled.h3`
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 800;
  color: ${darkPurple};
  display: flex;
  align-items: center;
  gap: 8px;

  @media (max-width: 768px) {
    font-size: 17px;
    margin: 0 0 10px 0;
  }

  @media (max-width: 480px) {
    font-size: 16px;
    margin: 0 0 8px 0;
    gap: 6px;

    svg {
      width: 20px;
      height: 20px;
    }
  }
`;

export const CardMeta = styled.div`
  margin-top: 8px;
  font-size: 14px;
  color: ${muted};
  font-weight: 600;
  line-height: 1.6;
  display: flex;
  flex-direction: column;
  gap: 6px;

  strong {
    color: #111827;
    font-weight: 800;
  }

  @media (max-width: 768px) {
    font-size: 13px;
    gap: 5px;
  }

  @media (max-width: 480px) {
    font-size: 12px;
    gap: 4px;
    margin-top: 6px;
  }
`;

export const MetaRow = styled.div`
  display: flex;
  align-items: center;
  gap: 6px;

  @media (max-width: 480px) {
    gap: 4px;

    svg {
      width: 14px;
      height: 14px;
    }
  }
`;

export const Badge = styled.span`
  padding: 8px 14px;
  border-radius: 16px;
  background: ${props => props.$active ? 'rgba(77, 182, 172, 0.14)' : 'rgba(239, 68, 68, 0.14)'};
  color: ${props => props.$active ? '#0f766e' : '#dc2626'};
  font-weight: 800;
  font-size: 13px;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid ${props => props.$active ? 'rgba(77, 182, 172, 0.3)' : 'rgba(239, 68, 68, 0.3)'};
  height: fit-content;

  @media (max-width: 768px) {
    padding: 7px 12px;
    font-size: 12px;
  }

  @media (max-width: 480px) {
    padding: 6px 10px;
    font-size: 11px;
    border-radius: 12px;
    align-self: flex-start;
  }
`;

export const EmptyState = styled.div`
  width: 100%;
  max-width: 1040px;
  background: white;
  border-radius: 20px;
  padding: 48px 24px;
  text-align: center;
  color: ${muted};
  font-weight: 700;
  border: 2px dashed #e5e7eb;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.06);

  @media (max-width: 768px) {
    padding: 40px 20px;
    border-radius: 16px;
  }

  @media (max-width: 480px) {
    padding: 32px 16px;
    border-radius: 14px;
  }
`;

export const EmptyText = styled.p`
  margin: 12px 0 0 0;
  color: ${muted};
  font-weight: 600;
  font-size: 15px;

  @media (max-width: 768px) {
    font-size: 14px;
    margin: 10px 0 0 0;
  }

  @media (max-width: 480px) {
    font-size: 13px;
    margin: 8px 0 0 0;
  }
`;

export const EmptyIcon = styled.div`
  font-size: 48px;
  margin-bottom: 8px;
  opacity: 0.5;

  @media (max-width: 768px) {
    font-size: 42px;
  }

  @media (max-width: 480px) {
    font-size: 36px;
    margin-bottom: 6px;
  }
`;

export const Footer = styled.div`
  width: 100%;
  max-width: 1040px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 32px;
  padding-bottom: 20px;

  @media (max-width: 768px) {
    margin-top: 24px;
    padding-bottom: 16px;
  }

  @media (max-width: 480px) {
    margin-top: 20px;
    padding-bottom: 12px;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    max-width: 100%;
    background: linear-gradient(180deg, transparent 0%, rgba(249, 250, 251, 0.98) 20%, rgba(249, 250, 251, 1) 100%);
    padding: 16px 12px 20px;
    margin-top: 0;
  }
`;

export const AddButton = styled.button`
  background: linear-gradient(135deg, ${darkPurple} 0%, #5a2591 100%);
  color: white;
  border: none;
  border-radius: 14px;
  padding: 14px 28px;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(107, 46, 158, 0.3);
  display: flex;
  align-items: center;
  gap: 8px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(107, 46, 158, 0.4);
  }

  &:active {
    transform: translateY(0);
  }

  @media (max-width: 768px) {
    padding: 13px 24px;
    font-size: 14px;
    border-radius: 12px;
  }

  @media (max-width: 480px) {
    padding: 12px 20px;
    font-size: 14px;
    border-radius: 12px;
    width: 100%;
    max-width: 320px;
    justify-content: center;

    svg {
      width: 18px;
      height: 18px;
    }
  }
`;

export const PriceTag = styled.span`
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 800;
  display: inline-flex;
  align-items: center;
  gap: 4px;

  @media (max-width: 768px) {
    padding: 4px 8px;
    font-size: 12px;
    border-radius: 6px;
  }

  @media (max-width: 480px) {
    padding: 3px 7px;
    font-size: 11px;
    border-radius: 6px;
  }
`;
