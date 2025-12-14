import styled from 'styled-components';
import { darkPurple } from '../../constants/colors';

export const Container = styled.div`
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
`;

export const OptionButton = styled.button`
  padding: 12px 24px;
  background-color: ${darkPurple};
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    opacity: 0.9;
    transform: scale(1.02);
  }

  &:active {
    transform: scale(0.98);
  }
`;
