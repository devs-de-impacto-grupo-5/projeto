import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { darkPurple } from '../../constants/colors';

export const Container = styled(Link)`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  background-color: white;
  border-radius: 16px;
  padding: 16px 16px;
  width: 100%;
  max-width: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
  text-decoration: none;
  gap: 16px;

  &:hover {
    transform: translateY(-2px);
  }
`;

export const IconWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: ${props => props.backgroundColor};
  flex-shrink: 0;
`;

export const IconContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
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
  color: ${darkPurple};
  margin: 0;
  text-align: left;
`;

export const Subtitle = styled.p`
  font-size: 14px;
  font-weight: 400;
  color: ${darkPurple};
  margin: 0;
  text-align: left;
  opacity: 0.8;
`;
