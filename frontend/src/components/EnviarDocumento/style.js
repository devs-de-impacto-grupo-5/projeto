import styled from 'styled-components';
import { darkPurple, lightGreen, darkGreen, lightPurple } from '../../constants/colors';

export const Container = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: ${props => props.type === 'pendente' ? 'pointer' : 'default'};
  transition: transform 0.2s;

  &:hover {
    transform: ${props => props.type === 'pendente' ? 'translateY(-2px)' : 'none'};
  }
`;

export const IconWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: ${props => props.type === 'enviado' ? lightGreen : lightPurple};
  flex-shrink: 0;
`;

export const TextContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
`;

export const Title = styled.h3`
  font-size: 16px;
  font-weight: 700;
  margin: 0;
`;

export const Subtitle = styled.p`
  font-size: 14px;
  font-weight: 400;
  color: ${props => props.type === 'enviado' ? darkGreen : darkPurple};
  margin: 0;
  opacity: 0.8;
`;

export const ActionIcon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${darkPurple};
  opacity: 0.5;
`;
