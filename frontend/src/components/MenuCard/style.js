import styled from 'styled-components';
import { darkPurple } from '../../constants/colors';

export const Container = styled.div`
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 20px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
  min-height: 120px;

  &:hover {
    transform: translateY(-2px);
  }
`;

export const Title = styled.h3`
  font-size: 16px;
  font-weight: 600;
  color: ${darkPurple};
  margin: 0;
`;

export const IconWrapper = styled.div`
  position: absolute;
  bottom: 0px;
  right: 0px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${props => props.color || darkPurple};
`;
