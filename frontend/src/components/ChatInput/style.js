import styled from 'styled-components';
import { darkPurple, neutral } from '../../constants/colors';

export const Container = styled.form`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background-color: ${neutral};
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
`;

export const Input = styled.input`
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 24px;
  font-size: 14px;
  outline: none;

  &::placeholder {
    color: #999;
  }

  &:focus {
    border-color: ${darkPurple};
  }
`;

export const SendButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: ${darkPurple};
  border: none;
  color: white;
  cursor: pointer;
  flex-shrink: 0;

  &:hover {
    opacity: 0.9;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;
