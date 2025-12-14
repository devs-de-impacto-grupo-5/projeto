import styled from 'styled-components';

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  background-color: #f5f5f5;
`;

export const Title = styled.h1`
  font-size: 2rem;
  color: #333;
  margin-bottom: 30px;
`;

export const Button = styled.button`
  width: 100%;
  max-width: 400px;
  padding: 14px;
  margin-top: 20px;
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: #0056b3;
  }

  &:active {
    transform: scale(0.98);
  }
`;
