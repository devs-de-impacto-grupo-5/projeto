import styled from 'styled-components';
import { lighnerPurple } from '../../constants/colors';

export const Container = styled.div`
  display: flex;
  align-items: flex-start;
  gap: 12px;
  width: 100%;
  max-width: 540px;
  margin-bottom: 20px;
`;

export const IconWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: ${lighnerPurple};
  flex-shrink: 0;
`;

export const MessageBox = styled.div`
  background-color: white;
  border-radius: 0 16px 16px 16px;
  padding: 16px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex: 1;
`;

export const MessageText = styled.p`
  font-size: 15px;
  font-weight: 400;
  margin: 0;
  line-height: 1.5;
  white-space: pre-line;
  word-wrap: break-word;
  overflow-wrap: break-word;
`;

export const TypingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 0;
`;

export const Dot = styled.div`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: ${lighnerPurple};
  animation: typing 1.4s infinite;
  animation-delay: ${props => props.delay};

  @keyframes typing {
    0%, 60%, 100% {
      transform: translateY(0);
      opacity: 0.7;
    }
    30% {
      transform: translateY(-10px);
      opacity: 1;
    }
  }
`;
