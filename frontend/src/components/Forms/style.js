import styled from 'styled-components';

export const FormContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 400px;
`;

export const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

export const Label = styled.label`
  font-size: 1rem;
  font-weight: 500;
  color: #333;
`;

export const Input = styled.input`
  padding: 12px 16px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s;

  &:focus {
    border-color: #007bff;
  }

  &::placeholder {
    color: #aaa;
  }
`;
