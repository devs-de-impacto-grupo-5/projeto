import styled from 'styled-components';
import { darkPurple } from '../../constants/colors';

const muted = '#6B7280';

export const FormRow = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
`;

export const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 6px;
`;

export const Label = styled.label`
  font-size: 14px;
  font-weight: 700;
  color: ${darkPurple};
  cursor: pointer;
  display: flex;
  align-items: center;

  input[type="checkbox"] {
    margin-right: 8px;
    cursor: pointer;
    width: 18px;
    height: 18px;
  }
`;

export const Input = styled.input`
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  transition: border-color 0.2s;

  &:focus {
    outline: none;
    border-color: ${darkPurple};
    box-shadow: 0 0 0 3px rgba(107, 46, 158, 0.1);
  }

  &::placeholder {
    color: ${muted};
  }
`;

export const Select = styled.select`
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s;

  &:focus {
    outline: none;
    border-color: ${darkPurple};
    box-shadow: 0 0 0 3px rgba(107, 46, 158, 0.1);
  }

  option {
    color: #1f2937;
  }
`;

export const Button = styled.button`
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  flex: 1;

  ${props => props.variant === 'primary' ? `
    background: ${darkPurple};
    color: white;

    &:hover:not(:disabled) {
      background: #5a2591;
      box-shadow: 0 4px 12px rgba(107, 46, 158, 0.3);
    }

    &:disabled {
      background: #d1d5db;
      cursor: not-allowed;
    }
  ` : `
    background: #f3f4f6;
    color: ${darkPurple};
    border: 1px solid #e5e7eb;

    &:hover:not(:disabled) {
      background: #e5e7eb;
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  `}
`;

export const ErrorMessage = styled.div`
  padding: 12px;
  margin-bottom: 16px;
  background: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #991b1b;
  font-size: 14px;
  font-weight: 600;
`;

export const SuccessMessage = styled.div`
  padding: 12px;
  margin-bottom: 16px;
  background: #dcfce7;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  color: #166534;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
`;
