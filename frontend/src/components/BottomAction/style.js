import styled from 'styled-components';
import { darkPurple, neutral } from '../../constants/colors';

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px;
  background-color: white;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
`;

export const Button = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  max-width: 400px;
  padding: 16px 24px;
  background-color: ${neutral};
  border: none;
  border-radius: 24px;
  cursor: pointer;
  transition: opacity 0.2s;

  &:hover {
    opacity: 0.9;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

export const ButtonText = styled.span`
  font-size: 16px;
  font-weight: 600;
  color: ${darkPurple};
`;

export const Description = styled.p`
  font-size: 12px;
  font-weight: 400;
  color: ${darkPurple};
  margin: 0;
  text-align: center;
  opacity: 0.7;
`;
