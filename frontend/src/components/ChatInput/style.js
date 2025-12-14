import styled from 'styled-components';
import { darkPurple, neutral } from '../../constants/colors';

export const Container = styled.form`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 -2px 14px rgba(0, 0, 0, 0.08);
  border-top: 1px solid #edf0f3;
  width: 100%;
  box-sizing: border-box;
  max-width: 1000px;
  border-radius: 16px;
`;

export const Input = styled.input`
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 999px;
  font-size: 14px;
  outline: none;

  &::placeholder {
    color: #999;
  }

  &:focus {
    border-color: ${darkPurple};
    box-shadow: 0 0 0 3px rgba(106, 58, 159, 0.15);
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
