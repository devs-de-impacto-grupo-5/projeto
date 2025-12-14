import styled from 'styled-components';
import { lightGreen, darkPurple } from '../../constants/colors';

export const Container = styled.div`
  display: flex;
  align-items: flex-start;
  gap: 12px;
  width: 100%;
  max-width: 540px;
  justify-content: flex-end;
`;

export const IconWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: ${lightGreen};
  flex-shrink: 0;
`;

export const MessageBox = styled.div`
  background-color: white;
  border-radius: 16px 0 16px 16px;
  padding: 16px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex: 1;
`;

export const MessageText = styled.p`
  font-size: 15px;
  font-weight: 400;
  margin: 0;
  line-height: 1.5;
`;
